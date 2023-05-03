from PyPDPM import HIPPS

def test_get_getReimbursementAmount():
    assert(HIPPS.getReimbursementAmount('AAAA1', 2) == 1447.57)
