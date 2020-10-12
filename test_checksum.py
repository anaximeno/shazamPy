from checksum import readinst


def test_exist_process():
    assert readinst.exists("testfiles/testfile.png") == True

