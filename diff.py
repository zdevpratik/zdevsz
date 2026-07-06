import sys
import difflib

f1 = open(sys.argv[1], encoding='utf-8').read().splitlines()
f2 = open(sys.argv[2], encoding='utf-8').read().splitlines()
diff = list(difflib.unified_diff(f1, f2, lineterm=''))
with open('diff.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(diff))
