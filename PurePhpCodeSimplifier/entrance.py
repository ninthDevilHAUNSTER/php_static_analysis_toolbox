from PurePhpCodeSimplifier.base import PurePhpCodeSimplifier as spas
import sys

if __name__ == '__main__':
    s = spas(input_path=sys.argv[1])
    s.do_simplify()
