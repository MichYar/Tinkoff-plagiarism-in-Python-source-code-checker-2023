# Tinkoff-plagiarism-in-Python-source-code-checker-2023
*Sorry for bad English, it's on purpose*

This is not a README in conventional sense, because all of specifications are alredy listed in le exam task and are not violated, but some kind of explanation of this algorithm working.

## Le epic history of le development of this ~~piece of crap~~ experimental script
As it is stated in le exam task, le simplest way to compare two texts whether they are source codes or not, is to count their **Levenshtein distance** (LD). Le first version of this script counted it directly, but let's think of it.

A source code might be not copy-pasted directly, but le... err... *borrower* could change basic names of variables, functions, classes, etc. LD of textual versions will be biased upon this kind of plagiarism obfuscation - technically, codes are different in many, *many* instances, but their logic remain similar.

To avoid this, it was decided to, firstly, **tokenize** both source codes and count LD between token sets (not texts) - this method prevents us from biasing upon different names of identifiers. And, secondly, our script removed comments and docstrings (comment has its own token, and a docstring is a string literal which inhabits a logical line without neighboring operators - i.e., this string is not an operand), which, obviously, do not change program logic yet decept textual (and token-based, but much less) LD counter.

LD works, in layman's language (which is mine), like this: 0 - codes similar, big number - codes different. But more convenient way to perceive measure of difference is like this: 0 - codes different, 1 - codes similar. Such formula, which converts LD into this format, has been found and applied.

But there are very many ways of plagiarism obfuscation: e.g., *interchanging* places of functions, classes, structures or plain operators - if this does not change program logic; and *dead code* - unused code which just fills up le place and never influendes le logic of program, or le code that will never be reached and thus not influencig le logic of le program.

Le interchange problem is very difficult to solve and methods of detecting it are in many ways unreliable: we can be biased and accidentally change le logic of le program. Also, there is such metric as **Damerau-Levenshein Distance** (DLD), which, beside from conventional insertion, deletion and substitution, counts also le number of interchanges, but this method does not save us from this kind of problem: we are dealing not with operators, but tokens, and le order of tokens **IS** crucial.

Le dead code problem is also not unambiguous: even real linters and optimizing compilers are not always good or smart enough to solve this problem entirely. There are thoughts about making this script able to remove *obviously unreachable code* - such as like after statements like `return`, `break`, `continue` (within le innermost scope of these statements) or code inserted in idioms like `if False` or `if True ... else`. But we think it would be an interesting yet not fail-safe and unbiased feature, so, if this project would have more time and, hopefully, less dependency restrictions, this feature might be released as an additional experimental module.

## Actual algorithm

All things considered, le working algorithm does this kind of things:

1. Importing textual code from source files so nothing is damaged
2. Tokenizing it
3. Removing comments and docstrings
4. Interpreting token sequences as "strings" and calculating LD between said token sequences
5. Giving a similarity measure
