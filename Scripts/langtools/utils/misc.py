"""Miscellaneous functions and classes."""
import sys

def ispunct(s):
    """Returns @c True, if all characters in @p s are punctuation marks."""
    for c in s:
        if c.isalnum():
            return False
    return True

# http://en.wikipedia.org/wiki/Quotation_mark_glyphs.
quotationMarks = frozenset(
        u'\u0022\u0027\u00AB\u00BB\u2018\u2019\u201A\u201B\u201C\u201D' +
        u'\u201E\u201F\u2039\u203A\u300C\u300D\u300E\u300F\u301D\u301E' +
        u'\u301F\uFE41\uFE42\uFE43\uFE44\uFF02\uFF07\uFF62\uFF63')
brackets = frozenset(
        u'\u00AB\u00BB\u2039\u203A\u0028\u0029\u005B\u005D\u003C\u003E' +
        u'\u007B\u007D\u2308\u2309\u230A\u230B\u27E8\u27E9\u2329\u232A' +
        u'\uFF62\uFF63\u3008\u3009\u300A\u300B\u300C\u300D\u300E\u300F' +
        u'\u3010\u3011\uFF08\uFF09\uFF3B\uFF3D\uFF1C\uFF1E\uFF5B\uFF5D')
# - and & are not quotation marks; nevertheless they have to be removed from the
# word 
otherStickyCharacters = frozenset(u'-&')
wikiGarbage = frozenset(u'|[]{}<>()*=')
quotationWikiGarbage = frozenset(quotationMarks | otherStickyCharacters | wikiGarbage)
empty_set = frozenset()

wikiRemove = set(u'|')

def isquot(s):
    """Returns @c True if all characters in @p s are quotation marks."""
    for c in s:
        if not c in quotationMarks:
            return False
    return True

def is_quote_or_garbage(s):
    """Returns @c True if all characters in @p s are quotation marks or wiki
    garbage."""
    for c in s:
        if not c in quotationWikiGarbage:
            return False
    return True

def remove_quot_from_word(token):
    """Removes quotation marks from the word and returns both the word and
    the removed quotation marks as separate tokens in a list."""
    return remove_unwanted_characters_from_word(token, quotationMarks)

def remove_quot_and_wiki_crap_from_word(token):
    """Removes quotation marks and wiki garbage characters from the word and
    returns both the word and the removed characters as separate tokens in a
    list."""
    return remove_unwanted_characters_from_word(
            token, quotationWikiGarbage) #, __wikiRemove)

def remove_unwanted_characters_from_word(token, unwanted_set, remove_set=None):
    """Removes the characters @p unwanted_set from around the word and
    returns both the word and the removed characters as separate tokens in a
    list."""
    if ispunct(token):
        return [token]
    else:
        if remove_set is None:
            remove_set = empty_set
        ret, after = [], []
        begin, end = 0, 0
        for i in xrange(0, len(token)):
            if token[i] in unwanted_set:
                if token[i] not in remove_set:
                    ret.append(token[i])
            else:
                begin = i
                break

        for i in xrange(len(token) - 1, begin - 1, -1):
            if token[i] in unwanted_set:
                if token[i] not in remove_set:
                    after.append(token[i])
            else:
                end = i + 1
                break

        ret.append(token[begin:end])
        after.reverse()
        ret += after

        return ret

def print_logging(text, stream=sys.stderr, encoding='utf-8'):
    """
    Prints @p text to and then flushes the stream. A newline is automatically
    appended to the output, as in print.
    """
    stream.write((unicode(text) + u"\n").encode(encoding))
    stream.flush()

