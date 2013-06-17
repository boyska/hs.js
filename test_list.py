from StringIO import StringIO
import re

import hsadmin

def test_format():
    hsadmin.out_buffer = StringIO()
    hsadmin.hs_list(None)
    for line in hsadmin.out_buffer.getvalue().split('\n'):
        print line
        url, binding, data = line.split('\t')
        assert re.match('^[a-z0-9]{16}\.onion:[\d+]', url)
        ip, port = binding.split(':')
        assert port.isdigit()
        parts = ip.split('.')
        assert len(parts) == 4
        for part in parts:
            assert 0 <= int(part) < 256
