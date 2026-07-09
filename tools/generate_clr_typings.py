import argparse
import glob
import keyword
import os
import shutil
from collections import defaultdict
from pathlib import Path

import clr

from System import AppDomain, MulticastDelegate
from System.Reflection import BindingFlags


# All CLR integer/floating widths map to plain int/float: pythonnet converts them to
# Python int/float at the boundary anyway, and distinct stub classes (e.g. Single as a
# float subclass) reject valid calls such as Add(0.5) through list invariance.
PYTHON_TYPE_NAMES = {
	"System.Boolean": "bool",
	"System.Byte": "int",
	"System.SByte": "int",
	"System.Int16": "int",
	"System.UInt16": "int",
	"System.Int32": "int",
	"System.UInt32": "int",
	"System.Int64": "int",
	"System.UInt64": "int",
	"System.Single": "float",
	"System.Double": "float",
	"System.Decimal": "float",
	"System.String": "str",
	"System.Void": "None",
}

# Names re-exported by the runtime FLImagingClrPy bridge (from System import *) that are
# used as generic type arguments in user code ("List[Double]()", "CFLPoint3[Single](...)").
# Aliasing them to int/float keeps those instantiations fully typed in the stubs.
NUMERIC_EXPORT_ALIASES = {
	"Boolean": "bool",
	"Byte": "int",
	"SByte": "int",
	"Int16": "int",
	"UInt16": "int",
	"Int32": "int",
	"UInt32": "int",
	"Int64": "int",
	"UInt64": "int",
	"Single": "float",
	"Double": "float",
	"Decimal": "float",
}

MAX_OVERLOADS_FOR_SIGNATURE_HELP = 10
ADDITIONAL_REPRESENTATIVE_OVERLOADS = 7

STUB_PACKAGE_NAMES = {
	"FLImagingCLR": "FLImagingCLR-stubs",
	"FLImagingClrPy": "FLImagingClrPy-stubs",
}

TYPE_SPECIFICITY_CACHE = {}

SYSTEM_EXPORTS = [
	"Boolean",
	"Byte",
	"SByte",
	"Int16",
	"UInt16",
	"Int32",
	"UInt32",
	"Int64",
	"UInt64",
	"Single",
	"Double",
	"Decimal",
	"Console",
	"String",
	"Object",
	"Enum",
	"Array",
	"List",
	"Dictionary",
	"StringBuilder",
]

# CLR operator method name -> Python dunder. Conversion (op_Implicit/op_Explicit) and
# op_Assign have no Python equivalent and are intentionally omitted.
OPERATOR_DUNDERS = {
	"op_Addition": "__add__",
	"op_Subtraction": "__sub__",
	"op_Multiply": "__mul__",
	"op_Division": "__truediv__",
	"op_Modulus": "__mod__",
	"op_BitwiseAnd": "__and__",
	"op_BitwiseOr": "__or__",
	"op_ExclusiveOr": "__xor__",
	"op_LeftShift": "__lshift__",
	"op_RightShift": "__rshift__",
	"op_UnaryNegation": "__neg__",
	"op_UnaryPlus": "__pos__",
	"op_OnesComplement": "__invert__",
	"op_Equality": "__eq__",
	"op_Inequality": "__ne__",
	"op_LessThan": "__lt__",
	"op_LessThanOrEqual": "__le__",
	"op_GreaterThan": "__gt__",
	"op_GreaterThanOrEqual": "__ge__",
}

# Dunders that Python defines on object as (self, object) -> bool. Narrowing the
# operand type here would both violate the supertype signature and reject valid
# comparisons (e.g. "x == None"), so keep the operand as object.
OBJECT_OPERAND_DUNDERS = {"__eq__", "__ne__"}

# System.Collections.Generic.List<T> appears in thousands of public signatures. It is
# declared once in the FLImagingCLR root stub (the runtime FLImagingCLR module does not
# have it, but only other stubs and FLImagingClrPy re-export reference it there).
# Surface below is what pythonnet actually supports: len/iter/index/in plus the List API.
# A Python list is NOT implicitly convertible to List<T>, hence no Iterable constructor.
LIST_STUB_LINES = [
	"_TList = TypeVar(\"_TList\")",
	"",
	"class List(Generic[_TList]):",
	"\t@overload",
	"\tdef __init__(self) -> None: ...",
	"\t@overload",
	"\tdef __init__(self, capacity: int) -> None: ...",
	"\t@overload",
	"\tdef __init__(self, collection: List[_TList]) -> None: ...",
	"\tCount: int",
	"\tdef Add(self, item: _TList) -> None: ...",
	"\tdef AddRange(self, collection: List[_TList]) -> None: ...",
	"\tdef Clear(self) -> None: ...",
	"\tdef Contains(self, item: _TList) -> bool: ...",
	"\tdef IndexOf(self, item: _TList) -> int: ...",
	"\tdef Insert(self, index: int, item: _TList) -> None: ...",
	"\tdef Remove(self, item: _TList) -> bool: ...",
	"\tdef RemoveAt(self, index: int) -> None: ...",
	"\tdef ToArray(self) -> list[_TList]: ...",
	"\tdef __contains__(self, item: object) -> bool: ...",
	"\tdef __getitem__(self, index: int) -> _TList: ...",
	"\tdef __setitem__(self, index: int, value: _TList) -> None: ...",
	"\tdef __iter__(self) -> Iterator[_TList]: ...",
	"\tdef __len__(self) -> int: ...",
	"",
]

SYSTEM_EXPORT_STUB_LINES = {
	"Console": [
		"class Console:",
		"\t@overload",
		"\t@staticmethod",
		"\tdef WriteLine(value: Any) -> None: ...",
		"\t@overload",
		"\t@staticmethod",
		"\tdef WriteLine(strFormat: str, arg0: Any, *args: Any) -> None: ...",
	],
	"Enum": [
		"class Enum:",
		"\t@staticmethod",
		"\tdef ToObject(enumType: Any, value: Any) -> Any: ...",
	],
	"StringBuilder": [
		"class StringBuilder:",
		"\t@overload",
		"\tdef __init__(self) -> None: ...",
		"\t@overload",
		"\tdef __init__(self, value: Any) -> None: ...",
		"\t@property",
		"\tdef Length(self) -> int: ...",
		"\tdef Append(self, value: Any) -> StringBuilder: ...",
		"\tdef Clear(self) -> StringBuilder: ...",
		"\tdef GetBuffer(self) -> Any: ...",
		"\tdef ToString(self) -> str: ...",
		"\tdef __str__(self) -> str: ...",
	],
}


class SAnnotationContext:
	def __init__(self, namespace):
		self.m_strNamespace = namespace
		self.m_setImportNamespaces = set()
		self.m_i32MaxTypeVar = -1
		self.m_listClassStack = []

	def NoteTypeVar(self, i32Index):
		if i32Index > self.m_i32MaxTypeVar:
			self.m_i32MaxTypeVar = i32Index

	def PushClass(self, tp):
		self.m_listClassStack.append(tp)

	def PopClass(self):
		self.m_listClassStack.pop()

	def GetCurrentGenericTypeArguments(self, tp):
		if not self.m_listClassStack:
			return []

		current = self.m_listClassStack[-1]
		if not current.IsGenericTypeDefinition or tp != current:
			return []

		args = []
		for i in range(len(current.GetGenericArguments())):
			self.NoteTypeVar(i)
			args.append(f"T{i}")
		return args

	def GetNamespaceAlias(self, namespace):
		if namespace == self.m_strNamespace:
			return ""

		self.m_setImportNamespaces.add(namespace)
		return "_" + namespace.replace(".", "_") + "."


class SGenerationStats:
	def __init__(self):
		self.m_dictTypeKinds = defaultdict(int)
		self.m_dictMemberCounts = defaultdict(int)
		self.m_dictFilterCounts = defaultdict(int)
		self.m_listWrittenFiles = []

	def NoteType(self, tp):
		if tp.IsEnum:
			self.m_dictTypeKinds["enums"] += 1
		elif IsDelegateType(tp):
			self.m_dictTypeKinds["delegates"] += 1
		else:
			self.m_dictTypeKinds["classes"] += 1

		if tp.IsGenericTypeDefinition:
			self.m_dictTypeKinds["generic classes"] += 1

	def NoteMember(self, name, count=1):
		self.m_dictMemberCounts[name] += count

	def NoteFilter(self, name, count=1):
		self.m_dictFilterCounts[name] += count

	def NoteFile(self, path, text):
		self.m_listWrittenFiles.append((len(text.splitlines()), path))

	def GetWrittenFileCount(self):
		return len(self.m_listWrittenFiles)

	def GetWrittenLineCount(self):
		return sum(i32LineCount for i32LineCount, path in self.m_listWrittenFiles)

	def GetGeneratedSignatureCount(self):
		names = ("constructors", "methods", "indexers", "operators")
		return sum(self.m_dictMemberCounts[name] for name in names)

	def GetLargestFiles(self, count):
		return sorted(self.m_listWrittenFiles, reverse=True)[:count]


def GetDefaultDllDir():
	if os.environ.get("PROCESSOR_ARCHITECTURE", "").endswith("64") or os.environ.get("PROCESSOR_ARCHITEW6432"):
		return Path(r"C:\Program Files\FLImaging\FLImaging\BinaryX64")
	return Path(r"C:\Program Files\FLImaging\FLImaging\Binary")


def CleanName(name):
	name = name.split("`", 1)[0]
	name = name.replace("+", "_")
	return name


def MakeIdentifier(name, fallback):
	if not name:
		name = fallback

	name = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in name)
	if not name or name[0].isdigit():
		name = "_" + name
	if keyword.iskeyword(name):
		name += "_"

	return name


def GetTypePath(tp):
	names = []
	current = tp
	while current is not None:
		names.append(CleanName(current.Name))
		current = current.DeclaringType

	return ".".join(reversed(names))


def HasUncallablePointerType(tp):
	if tp is None:
		return False

	if tp.IsByRef or tp.IsArray:
		return HasUncallablePointerType(tp.GetElementType())

	# pythonnet has no pointer marshaling, so no T* signature (native C++ class, CResult*,
	# double*, ...) is callable from Python. Emitting them produces "Any" overloads that
	# shadow the real managed overloads during type checking.
	return bool(tp.IsPointer)


def HasUncallablePointerSignature(member):
	if hasattr(member, "ReturnType") and HasUncallablePointerType(member.ReturnType):
		return True

	for parameter in member.GetParameters():
		if HasUncallablePointerType(parameter.ParameterType):
			return True

	return False


def IsEmittableType(tp):
	# Matches assembly.GetExportedTypes(): a type is emitted only when it and every
	# enclosing type are publicly visible. Non-public types are skipped during
	# collection, so annotating with their name would reference an undefined symbol.
	if tp.IsGenericParameter:
		return True
	if tp.IsGenericType and not tp.IsGenericTypeDefinition:
		tp = tp.GetGenericTypeDefinition()

	current = tp
	while current is not None:
		if current.DeclaringType is None:
			if not current.IsPublic:
				return False
		elif not current.IsNestedPublic:
			return False
		current = current.DeclaringType

	return True


def GetTypeAnnotation(tp, context):
	if tp is None:
		return "Any"

	if tp.IsByRef:
		tp = tp.GetElementType()

	if tp.IsPointer:
		return "Any"

	if tp.IsArray:
		# Managed CLR arrays (cli::array) surface as sequences in pythonnet, so recover
		# the element type for the common rank-1 case. Multidimensional arrays use tuple
		# indexing (not list-like), so leave them as Any.
		if tp.GetArrayRank() == 1:
			return f"list[{GetTypeAnnotation(tp.GetElementType(), context)}]"
		return "Any"

	full_name = tp.FullName
	if full_name in PYTHON_TYPE_NAMES:
		return PYTHON_TYPE_NAMES[full_name]

	if tp.IsGenericParameter:
		try:
			position = tp.GenericParameterPosition
		except Exception:
			position = -1
		if position >= 0:
			context.NoteTypeVar(position)
			return f"T{position}"
		return "Any"

	if tp.IsGenericType and not tp.IsGenericTypeDefinition:
		generic_type = tp.GetGenericTypeDefinition()
		if generic_type.FullName == "System.Collections.Generic.List`1":
			element = GetTypeAnnotation(tp.GetGenericArguments()[0], context)
			return f"{context.GetNamespaceAlias('FLImagingCLR')}List[{element}]"
		if generic_type.Namespace and generic_type.Namespace.startswith("FLImagingCLR"):
			if not IsEmittableType(generic_type):
				return "Any"
			type_name = context.GetNamespaceAlias(generic_type.Namespace) + GetTypePath(generic_type)
			# Types nested in a generic parent are surfaced as non-generic in the stub
			# (enums / opaque classes), so they must not carry the parent's type args.
			if generic_type.DeclaringType is not None:
				return type_name
			generic_args = ", ".join(GetTypeAnnotation(arg, context) for arg in tp.GetGenericArguments())
			return f"{type_name}[{generic_args}]"

	if tp.IsGenericTypeDefinition and tp.Namespace and tp.Namespace.startswith("FLImagingCLR"):
		if not IsEmittableType(tp):
			return "Any"
		type_name = context.GetNamespaceAlias(tp.Namespace) + GetTypePath(tp)
		if tp.DeclaringType is not None:
			return type_name
		generic_args = context.GetCurrentGenericTypeArguments(tp)
		if generic_args:
			return f"{type_name}[{', '.join(generic_args)}]"
		return type_name

	if tp.Namespace and tp.Namespace.startswith("FLImagingCLR"):
		if not IsEmittableType(tp):
			return "Any"
		return context.GetNamespaceAlias(tp.Namespace) + GetTypePath(tp)

	return "Any"


def GetBaseClassAnnotation(tp, context):
	try:
		base_type = tp.BaseType
	except Exception:
		return None

	if base_type is None:
		return None
	if base_type.FullName in {"System.Object", "System.ValueType", "System.Enum"}:
		return None
	if not IsTargetType(base_type):
		return None

	annotation = GetTypeAnnotation(base_type, context)
	return None if annotation == "Any" else annotation


def FormatParameter(parameter, index, context):
	name = MakeIdentifier(parameter.Name, f"arg{index}")
	annotation = GetTypeAnnotation(parameter.ParameterType, context)
	if parameter.IsOptional or parameter.HasDefaultValue:
		return f"{name}: {annotation} = ..."
	return f"{name}: {annotation}"


def FormatParameterItems(parameters, include_self, context):
	items = []
	if include_self:
		items.append("self")

	for index, parameter in enumerate(parameters):
		items.append(FormatParameter(parameter, index, context))

	return items


def FormatParameters(parameters, include_self, context):
	items = FormatParameterItems(parameters, include_self, context)
	return ", ".join(items)


def GetCommonPrefix(items_list):
	if not items_list:
		return []

	prefix = []
	for index, item in enumerate(items_list[0]):
		if all(len(items) > index and items[index] == item for items in items_list):
			prefix.append(item)
		else:
			break

	return prefix


def AppendSignature(lines, indent, decorators, signature, overloaded):
	for decorator in decorators:
		lines.append(f"{indent}{decorator}")
	if overloaded:
		lines.append(f"{indent}@overload")
	lines.append(f"{indent}{signature}")


def GetRepresentativeIndices(count):
	if count <= MAX_OVERLOADS_FOR_SIGNATURE_HELP:
		return list(range(count))
	if count <= 2:
		return list(range(count))

	middle_indices = list(range(1, count - 1))
	selected = {0, count - 1}
	if len(middle_indices) <= ADDITIONAL_REPRESENTATIVE_OVERLOADS:
		selected.update(middle_indices)
	else:
		i32LastMiddle = len(middle_indices) - 1
		for i in range(ADDITIONAL_REPRESENTATIVE_OVERLOADS):
			if ADDITIONAL_REPRESENTATIVE_OVERLOADS == 1:
				i32SampleIndex = i32LastMiddle // 2
			else:
				i32SampleIndex = int((i * i32LastMiddle / (ADDITIONAL_REPRESENTATIVE_OVERLOADS - 1)) + 0.5)
			selected.add(middle_indices[i32SampleIndex])

		i32Cursor = 0
		while len(selected) < ADDITIONAL_REPRESENTATIVE_OVERLOADS + 2 and i32Cursor < len(middle_indices):
			selected.add(middle_indices[i32Cursor])
			i32Cursor += 1

	return sorted(selected)


def GetRepresentativeEntries(entries):
	return [entries[index] for index in GetRepresentativeIndices(len(entries))]


def FormatReturnType(method, context):
	return_type = GetTypeAnnotation(method.ReturnType, context)
	byref_return_types = [
		GetTypeAnnotation(parameter.ParameterType, context)
		for parameter in method.GetParameters()
		if parameter.ParameterType.IsByRef
	]

	if not byref_return_types:
		return return_type

	if return_type == "None":
		if len(byref_return_types) == 1:
			return byref_return_types[0]
		return "tuple[" + ", ".join(byref_return_types) + "]"

	return "tuple[" + ", ".join([return_type] + byref_return_types) + "]"


def GetComparableParameterType(tp):
	if tp is None:
		return None
	if tp.IsByRef:
		return GetComparableParameterType(tp.GetElementType())
	return tp


def IsCollapsibleReferenceType(tp):
	return tp is not None and tp.Namespace and tp.Namespace.startswith("FLImagingCLR") and not tp.IsValueType


def IsSameClrType(lhs, rhs):
	if lhs is None or rhs is None:
		return lhs is rhs
	if lhs == rhs:
		return True
	return lhs.FullName == rhs.FullName


def IsAtLeastAsSpecificType(candidate, base):
	candidate = GetComparableParameterType(candidate)
	base = GetComparableParameterType(base)
	if IsSameClrType(candidate, base):
		return True
	if not IsCollapsibleReferenceType(candidate) or not IsCollapsibleReferenceType(base):
		return False

	key = (candidate.FullName, base.FullName)
	if key in TYPE_SPECIFICITY_CACHE:
		return TYPE_SPECIFICITY_CACHE[key]

	try:
		result = base.IsAssignableFrom(candidate)
	except Exception:
		result = False

	TYPE_SPECIFICITY_CACHE[key] = result
	return result


def IsStrictlyMoreSpecificParameterTypes(candidate_types, base_types):
	if len(candidate_types) != len(base_types):
		return False

	bStrict = False
	for candidate_type, base_type in zip(candidate_types, base_types):
		if not IsAtLeastAsSpecificType(candidate_type, base_type):
			return False
		if not IsSameClrType(candidate_type, base_type):
			bStrict = True

	return bStrict


def IsStrictlyMoreSpecificMember(candidate, base):
	candidate_types = [GetComparableParameterType(parameter.ParameterType) for parameter in candidate.GetParameters()]
	base_types = [GetComparableParameterType(parameter.ParameterType) for parameter in base.GetParameters()]
	return IsStrictlyMoreSpecificParameterTypes(candidate_types, base_types)


def ReduceLessSpecificMethodOverloads(methods, stats=None):
	groups = defaultdict(list)
	parameter_type_cache = {}
	for index, method in enumerate(methods):
		parameter_type_cache[index] = [GetComparableParameterType(parameter.ParameterType) for parameter in method.GetParameters()]
		groups[(method.IsStatic, len(parameter_type_cache[index]))].append((index, method))

	less_specific_indices = set()
	for group in groups.values():
		if len(group) < 2:
			continue
		if not any(IsCollapsibleReferenceType(tp) for index, method in group for tp in parameter_type_cache[index]):
			continue

		for index, method in group:
			for other_index, other in group:
				if index == other_index:
					continue
				if IsStrictlyMoreSpecificParameterTypes(parameter_type_cache[other_index], parameter_type_cache[index]):
					less_specific_indices.add(index)
					break

	if stats is not None and less_specific_indices:
		stats.NoteFilter("less-specific overloads collapsed", len(less_specific_indices))

	return [method for index, method in enumerate(methods) if index not in less_specific_indices]


def LoadAssemblies(dll_dir):
	if hasattr(os, "add_dll_directory"):
		os.add_dll_directory(str(dll_dir))

	pattern = "FLImaging*X64CLR.dll" if "X64" in dll_dir.name.upper() else "FLImaging*X86CLR.dll"
	loaded = []
	failed = []

	for path in sorted(glob.glob(str(dll_dir / pattern))):
		try:
			clr.AddReference(path)
			loaded.append(Path(path).name)
		except Exception as ex:
			message = str(ex).splitlines()[0] if str(ex) else type(ex).__name__
			failed.append((Path(path).name, message))

	return loaded, failed


def IsTargetAssembly(assembly):
	return assembly.GetName().Name.startswith("FLImaging")


def IsTargetType(tp):
	return tp.Namespace and tp.Namespace.startswith("FLImagingCLR")


def CollectTypes():
	types_by_namespace = defaultdict(list)

	for assembly in AppDomain.CurrentDomain.GetAssemblies():
		if not IsTargetAssembly(assembly):
			continue

		try:
			types = assembly.GetExportedTypes()
		except Exception:
			continue

		for tp in types:
			if not IsTargetType(tp):
				continue

			if tp.DeclaringType is not None:
				continue

			types_by_namespace[tp.Namespace].append(tp)

	return {namespace: sorted(types, key=lambda t: CleanName(t.Name)) for namespace, types in types_by_namespace.items()}


def GetNestedTypes(tp):
	try:
		return sorted(tp.GetNestedTypes(BindingFlags.Public), key=lambda t: CleanName(t.Name))
	except Exception:
		return []


def IsDelegateType(tp):
	try:
		return tp.IsSubclassOf(MulticastDelegate)
	except Exception:
		return False


def GetEnumMembers(tp):
	try:
		return [str(name) for name in tp.GetEnumNames()]
	except Exception:
		return []


def GetConstructors(tp, stats=None):
	try:
		constructors = list(tp.GetConstructors(BindingFlags.Public | BindingFlags.Instance))
	except Exception:
		return []

	result = []
	for constructor in constructors:
		if HasUncallablePointerSignature(constructor):
			if stats is not None:
				stats.NoteFilter("uncallable pointer signatures")
			continue
		result.append(constructor)

	return result


def GetPublicMethods(tp, stats=None):
	try:
		methods = tp.GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly)
	except Exception:
		return []

	result = []
	for method in methods:
		if method.IsSpecialName:
			continue
		if method.DeclaringType is not None and method.DeclaringType.FullName == "System.Object":
			continue
		if HasUncallablePointerSignature(method):
			if stats is not None:
				stats.NoteFilter("uncallable pointer signatures")
			continue
		result.append(method)

	return sorted(result, key=lambda m: (m.Name, len(m.GetParameters()), str(m)))


def GetOperatorMethods(tp, stats=None):
	try:
		methods = tp.GetMethods(BindingFlags.Public | BindingFlags.Static | BindingFlags.DeclaredOnly)
	except Exception:
		return []

	result = []
	for method in methods:
		if not method.IsSpecialName:
			continue
		if method.Name not in OPERATOR_DUNDERS:
			continue
		if HasUncallablePointerSignature(method):
			if stats is not None:
				stats.NoteFilter("uncallable pointer signatures")
			continue
		result.append(method)

	return sorted(result, key=lambda m: (m.Name, len(m.GetParameters()), str(m)))


def GetProperties(tp):
	try:
		return sorted(tp.GetProperties(BindingFlags.Public | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly), key=lambda p: p.Name)
	except Exception:
		return []


def GetFields(tp):
	try:
		return sorted(tp.GetFields(BindingFlags.Public | BindingFlags.Instance | BindingFlags.Static | BindingFlags.DeclaredOnly), key=lambda f: f.Name)
	except Exception:
		return []


def AppendEnum(lines, tp, indent=""):
	name = CleanName(tp.Name)
	lines.append(f"{indent}class {name}(IntEnum):")

	members = GetEnumMembers(tp)
	if not members:
		lines.append(f"{indent}\t...")
		return

	for member in members:
		lines.append(f"{indent}\t{MakeIdentifier(member, 'Value')} = ...")


def AppendMethodGroup(lines, name, methods, indent, context, stats):
	methods = ReduceLessSpecificMethodOverloads(methods, stats)
	seen = set()
	formatted = []

	for method in methods:
		parameter_items = FormatParameterItems(method.GetParameters(), include_self=not method.IsStatic, context=context)
		parameters = ", ".join(parameter_items)
		return_type = FormatReturnType(method, context)
		decorators = []
		if method.IsStatic:
			decorators.append("@staticmethod")

		signature = f"def {MakeIdentifier(name, 'Method')}({parameters}) -> {return_type}: ..."
		key = (tuple(decorators), signature)
		if key in seen:
			continue
		seen.add(key)
		formatted.append({
			"decorators": decorators,
			"signature": signature,
			"parameter_items": parameter_items,
			"return_type": return_type,
			"is_static": method.IsStatic,
		})

	if len(formatted) > MAX_OVERLOADS_FOR_SIGNATURE_HELP:
		stats.NoteFilter("overload groups summarized")
		static_values = {entry["is_static"] for entry in formatted}
		return_types = {entry["return_type"] for entry in formatted}
		return_type = next(iter(return_types)) if len(return_types) == 1 else "Any"
		prefix = GetCommonPrefix([entry["parameter_items"] for entry in formatted])
		if static_values != {True} and (not prefix or prefix[0] != "self"):
			prefix.insert(0, "self")

		fallback_parameters = ", ".join(prefix + ["*args: Any"])
		fallback_decorators = ["@staticmethod"] if static_values == {True} else []
		fallback_signature = f"def {MakeIdentifier(name, 'Method')}({fallback_parameters}) -> {return_type}: ..."

		collapsed = GetRepresentativeEntries(formatted) + [{
			"decorators": fallback_decorators,
			"signature": fallback_signature,
		}]
		collapsed_seen = set()
		for entry in collapsed:
			key = (tuple(entry["decorators"]), entry["signature"])
			if key in collapsed_seen:
				continue
			collapsed_seen.add(key)
			AppendSignature(lines, indent, entry["decorators"], entry["signature"], overloaded=True)
			stats.NoteMember("methods")
		return

	if len(formatted) > 1:
		for entry in formatted:
			AppendSignature(lines, indent, entry["decorators"], entry["signature"], overloaded=True)
			stats.NoteMember("methods")
	else:
		for entry in formatted:
			AppendSignature(lines, indent, entry["decorators"], entry["signature"], overloaded=False)
			stats.NoteMember("methods")


def AppendConstructorGroup(lines, constructors, indent, context, stats):
	seen = set()
	formatted = []

	for constructor in constructors:
		parameter_items = FormatParameterItems(constructor.GetParameters(), include_self=True, context=context)
		parameters = ", ".join(parameter_items)
		signature = f"def __init__({parameters}) -> None: ..."
		if signature in seen:
			continue
		seen.add(signature)
		formatted.append({
			"signature": signature,
			"parameter_items": parameter_items,
		})

	if len(formatted) > MAX_OVERLOADS_FOR_SIGNATURE_HELP:
		stats.NoteFilter("overload groups summarized")
		prefix = GetCommonPrefix([entry["parameter_items"] for entry in formatted])
		if not prefix or prefix[0] != "self":
			prefix.insert(0, "self")

		fallback_parameters = ", ".join(prefix + ["*args: Any"])
		fallback_signature = f"def __init__({fallback_parameters}) -> None: ..."
		collapsed = GetRepresentativeEntries(formatted) + [{"signature": fallback_signature}]
		collapsed_seen = set()
		for entry in collapsed:
			if entry["signature"] in collapsed_seen:
				continue
			collapsed_seen.add(entry["signature"])
			AppendSignature(lines, indent, [], entry["signature"], overloaded=True)
			stats.NoteMember("constructors")
		return

	if len(formatted) > 1:
		for entry in formatted:
			AppendSignature(lines, indent, [], entry["signature"], overloaded=True)
			stats.NoteMember("constructors")
	else:
		for entry in formatted:
			AppendSignature(lines, indent, [], entry["signature"], overloaded=False)
			stats.NoteMember("constructors")


def AppendOperatorGroup(lines, dunder, methods, indent, context, stats):
	# CLR operators are static (lhs, rhs); pythonnet exposes them as instance dunders,
	# so the first operand becomes self and the rest become the dunder arguments.
	seen = set()
	formatted = []

	for method in methods:
		rest = list(method.GetParameters())[1:]
		items = ["self"]
		for index, parameter in enumerate(rest):
			if dunder in OBJECT_OPERAND_DUNDERS:
				items.append(f"{MakeIdentifier(parameter.Name, f'arg{index}')}: object")
			else:
				items.append(FormatParameter(parameter, index, context))

		signature = f"def {dunder}({', '.join(items)}) -> {FormatReturnType(method, context)}: ..."
		if signature in seen:
			continue
		seen.add(signature)
		formatted.append(signature)

	overloaded = len(formatted) > 1
	for signature in formatted:
		AppendSignature(lines, indent, [], signature, overloaded=overloaded)
		stats.NoteMember("operators")


def AppendIndexer(lines, prop, index_params, indent, context, stats):
	value_type = GetTypeAnnotation(prop.PropertyType, context)
	if len(index_params) == 1:
		key_item = FormatParameter(index_params[0], 0, context)
	else:
		key_types = ", ".join(GetTypeAnnotation(parameter.ParameterType, context) for parameter in index_params)
		key_item = f"key: tuple[{key_types}]"
	if prop.CanRead:
		lines.append(f"{indent}def __getitem__(self, {key_item}) -> {value_type}: ...")
		stats.NoteMember("indexers")
	if prop.CanWrite:
		lines.append(f"{indent}def __setitem__(self, {key_item}, value: {value_type}) -> None: ...")
		stats.NoteMember("indexers")


def AppendDelegate(lines, tp, indent, context, stats):
	# pythonnet does not convert a bare Python callable at a delegate-typed parameter;
	# the caller must wrap it in the delegate type ("Delegate_X(handler)"). Expose that
	# constructor, typed from the delegate's Invoke signature.
	name = CleanName(tp.Name)
	lines.append(f"{indent}class {name}:")

	invoke = None
	try:
		invoke = tp.GetMethod("Invoke")
	except Exception:
		pass

	if invoke is None:
		lines.append(f"{indent}\tdef __init__(self, handler: Callable[..., Any]) -> None: ...")
		stats.NoteMember("constructors")
		return

	parameters = list(invoke.GetParameters())
	if any(parameter.ParameterType.IsByRef for parameter in parameters):
		handler_type = "Callable[..., Any]"
	else:
		parameter_types = ", ".join(GetTypeAnnotation(parameter.ParameterType, context) for parameter in parameters)
		handler_type = f"Callable[[{parameter_types}], {GetTypeAnnotation(invoke.ReturnType, context)}]"

	lines.append(f"{indent}\tdef __init__(self, handler: {handler_type}) -> None: ...")
	stats.NoteMember("constructors")


def AppendClass(lines, tp, context, stats, indent=""):
	context.PushClass(tp)
	name = CleanName(tp.Name)
	generic_argument_count = len(tp.GetGenericArguments()) if tp.IsGenericTypeDefinition else 0
	bases = []
	base_class = GetBaseClassAnnotation(tp, context)
	if base_class:
		bases.append(base_class)

	if generic_argument_count > 0:
		for i in range(generic_argument_count):
			context.NoteTypeVar(i)
		args = ", ".join(f"T{i}" for i in range(generic_argument_count))
		bases.append(f"Generic[{args}]")

	base = f"({', '.join(bases)})" if bases else ""
	lines.append(f"{indent}class {name}{base}:")
	body_indent = indent + "\t"
	body_start = len(lines)

	for nested in GetNestedTypes(tp):
		if nested.IsEnum:
			AppendEnum(lines, nested, indent=body_indent)
		elif IsDelegateType(nested):
			AppendDelegate(lines, nested, body_indent, context, stats)
		elif tp.IsGenericTypeDefinition:
			# A class nested in a generic parent cannot redeclare the parent's TypeVars
			# in its own Generic[...] list, so it stays opaque (currently only enums
			# exist under generic parents; this branch is a guard).
			lines.append(f"{body_indent}class {CleanName(nested.Name)}:")
			lines.append(f"{body_indent}\t...")
		else:
			AppendClass(lines, nested, context, stats, indent=body_indent)

	AppendConstructorGroup(lines, GetConstructors(tp, stats), body_indent, context, stats)

	for field in GetFields(tp):
		if field.IsSpecialName:
			continue
		lines.append(f"{body_indent}{MakeIdentifier(field.Name, 'field')}: {GetTypeAnnotation(field.FieldType, context)}")
		stats.NoteMember("fields")

	for prop in GetProperties(tp):
		index_params = list(prop.GetIndexParameters())
		if index_params:
			AppendIndexer(lines, prop, index_params, body_indent, context, stats)
			continue
		lines.append(f"{body_indent}{MakeIdentifier(prop.Name, 'property')}: {GetTypeAnnotation(prop.PropertyType, context)}")
		stats.NoteMember("properties")

	methods_by_name = defaultdict(list)
	for method in GetPublicMethods(tp, stats):
		methods_by_name[method.Name].append(method)

	for method_name in sorted(methods_by_name):
		AppendMethodGroup(lines, method_name, methods_by_name[method_name], body_indent, context, stats)

	operators_by_dunder = defaultdict(list)
	for method in GetOperatorMethods(tp, stats):
		operators_by_dunder[OPERATOR_DUNDERS[method.Name]].append(method)

	for dunder in sorted(operators_by_dunder):
		AppendOperatorGroup(lines, dunder, operators_by_dunder[dunder], body_indent, context, stats)

	if len(lines) == body_start:
		lines.append(f"{body_indent}...")

	context.PopClass()


def BuildModuleContent(namespace, types, stats):
	context = SAnnotationContext(namespace)
	body_lines = []

	export_names = []
	for tp in types:
		name = CleanName(tp.Name)
		export_names.append(name)
		if tp.IsEnum:
			AppendEnum(body_lines, tp)
		elif IsDelegateType(tp):
			AppendDelegate(body_lines, tp, "", context, stats)
		else:
			AppendClass(body_lines, tp, context, stats)
		body_lines.append("")

	lines = [
		"# This file is generated by tools/generate_clr_typings.py.",
		"from __future__ import annotations",
		"",
		"from enum import IntEnum",
		"from typing import Any, Callable, Generic, Iterator, TypeVar, overload",
	]

	for import_namespace in sorted(context.m_setImportNamespaces):
		lines.append(f"import {import_namespace} as _{import_namespace.replace('.', '_')}")

	lines.append("")
	if context.m_i32MaxTypeVar >= 0:
		for i in range(context.m_i32MaxTypeVar + 1):
			lines.append(f"T{i} = TypeVar(\"T{i}\")")
		lines.append("")

	if namespace == "FLImagingCLR":
		export_names.append("List")
		lines.extend(LIST_STUB_LINES)

	lines.extend(body_lines)
	lines.append(f"__all__ = {export_names!r}")
	lines.append("")
	return "\n".join(lines)


def NamespaceToStubParts(namespace):
	parts = namespace.split(".")
	if parts and parts[0] in STUB_PACKAGE_NAMES:
		parts[0] = STUB_PACKAGE_NAMES[parts[0]]
	return parts


def NamespaceToPath(output_dir, namespace):
	parts = NamespaceToStubParts(namespace)
	return output_dir.joinpath(*parts, "__init__.pyi")


def WriteText(path, text, stats=None):
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(text, encoding="utf-8-sig", newline="\r\n")
	if stats is not None:
		stats.NoteFile(path, text)


def WritePackageInitializers(output_dir, namespaces, stats):
	parts_seen = set()
	for namespace in namespaces:
		parts = NamespaceToStubParts(namespace)
		for index in range(1, len(parts)):
			parts_seen.add(tuple(parts[:index]))

	for parts in sorted(parts_seen):
		path = output_dir.joinpath(*parts, "__init__.pyi")
		if path.exists():
			continue
		WriteText(path, "# This file is generated by tools/generate_clr_typings.py.\n", stats)


def WriteFLImagingClrPyStub(output_dir, namespaces, types_by_namespace, stats):
	lines = [
		"# This file is generated by tools/generate_clr_typings.py.",
		"from __future__ import annotations",
		"",
		"from typing import Any, overload",
		"",
	]

	export_names = []
	for namespace in sorted(namespaces):
		if namespace != "FLImagingCLR" and not namespace.startswith("FLImagingCLR."):
			continue
		for tp in types_by_namespace[namespace]:
			name = CleanName(tp.Name)
			export_names.append(name)
			lines.append(f"from {namespace} import {name} as {name}")

	lines.append("")
	for name in SYSTEM_EXPORTS:
		export_names.append(name)
		if name in NUMERIC_EXPORT_ALIASES:
			lines.append(f"{name} = {NUMERIC_EXPORT_ALIASES[name]}")
			continue
		if name == "List":
			lines.append("from FLImagingCLR import List as List")
			continue
		if name in SYSTEM_EXPORT_STUB_LINES:
			lines.extend(SYSTEM_EXPORT_STUB_LINES[name])
			continue
		lines.append(f"{name}: Any")

	lines.append("")
	lines.append(f"__all__ = {sorted(set(export_names))!r}")
	lines.append("")
	WriteText(output_dir / STUB_PACKAGE_NAMES["FLImagingClrPy"] / "__init__.pyi", "\n".join(lines), stats)


def GenerateTypings(output_dir, clear):
	if clear and output_dir.exists():
		shutil.rmtree(output_dir)

	stats = SGenerationStats()
	types_by_namespace = CollectTypes()
	for namespace, types in types_by_namespace.items():
		for tp in types:
			stats.NoteType(tp)
		WriteText(NamespaceToPath(output_dir, namespace), BuildModuleContent(namespace, types, stats), stats)

	WritePackageInitializers(output_dir, types_by_namespace.keys(), stats)
	WriteFLImagingClrPyStub(output_dir, types_by_namespace.keys(), types_by_namespace, stats)
	return types_by_namespace, stats


def FormatOutputPath(path, output_dir):
	try:
		return str(path.relative_to(output_dir))
	except ValueError:
		return str(path)


def PrintGenerationStats(output_dir, types_by_namespace, stats):
	print(f"Generated files: {stats.GetWrittenFileCount()}")
	print(f"Generated lines: {stats.GetWrittenLineCount()}")
	print(f"Generated signatures: {stats.GetGeneratedSignatureCount()}")

	print("Types by namespace:")
	for namespace, types in sorted(types_by_namespace.items()):
		print(f"  {namespace}: {len(types)}")

	print("Type kinds:")
	for name in ("classes", "enums", "delegates", "generic classes"):
		print(f"  {name}: {stats.m_dictTypeKinds[name]}")

	print("Members emitted:")
	for name in ("constructors", "methods", "properties", "fields", "indexers", "operators"):
		print(f"  {name}: {stats.m_dictMemberCounts[name]}")

	print("Filtered:")
	for name in ("uncallable pointer signatures", "less-specific overloads collapsed", "overload groups summarized"):
		print(f"  {name}: {stats.m_dictFilterCounts[name]}")

	print("Largest files:")
	for i32LineCount, path in stats.GetLargestFiles(5):
		print(f"  {FormatOutputPath(path, output_dir)}: {i32LineCount} lines")


def main():
	repo_examples_dir = Path(__file__).resolve().parents[1]

	parser = argparse.ArgumentParser(description="Generate .pyi stubs for FLImaging CLR assemblies.")
	parser.add_argument("--dll-dir", type=Path, default=GetDefaultDllDir())
	parser.add_argument("--out", type=Path, default=repo_examples_dir / "typings")
	parser.add_argument("--no-clear", action="store_true", help="Do not delete the output directory before generation.")
	args = parser.parse_args()

	loaded, failed = LoadAssemblies(args.dll_dir)
	types_by_namespace, stats = GenerateTypings(args.out, clear=not args.no_clear)

	type_count = sum(len(types) for types in types_by_namespace.values())
	print(f"Loaded assemblies: {len(loaded)}")
	for name in loaded:
		print(f"  {name}")

	if failed:
		print(f"Skipped assemblies: {len(failed)}")
		for name, message in failed:
			print(f"  {name}: {message}")

	print(f"Generated namespaces: {len(types_by_namespace)}")
	print(f"Generated types: {type_count}")
	PrintGenerationStats(args.out, types_by_namespace, stats)
	print(f"Output: {args.out}")


if __name__ == "__main__":
	main()
