import unittest, threading, queue, time

from gridable import GridModifyLock, GridReadLock


class TestThreadLock(unittest.TestCase):
    def setUp(self):

        self.q = queue.Queue()
        self.readers = 0
        self.writers = 0

        def do_writing():
            self.writers = self.writers + 1
            self.assertEqual(self.readers, 0)
            self.assertGreaterEqual(self.writers, 1)
            time.sleep(0.25)
            self.writers = self.writers - 1

        def do_reading():
            self.readers = self.readers + 1
            self.assertEqual(self.writers, 0)
            self.assertGreaterEqual(self.readers, 1)
            time.sleep(0.25)
            self.readers = self.readers - 1

        def do_fail():
            raise Exception()

        self.do_safe_writing = GridModifyLock(do_writing)
        self.do_safe_reading = GridReadLock(do_reading)

        self.do_safe_writing_fail = GridModifyLock(do_fail)
        self.do_safe_reading_fail = GridReadLock(do_fail)

        def worker():
            while True:
                try:
                    task = self.q.get()
                    task[0]()
                finally:
                    self.q.task_done()

        for _ in range(3):
            threading.Thread(target=worker, daemon=True).start()

    def test_read(self):

        self.do_safe_reading()

        self.assertEqual(self.writers, 0)
        self.assertEqual(self.readers, 0)

    def test_write_than_read(self):

        self.q.put((self.do_safe_writing, ()))
        self.q.put((self.do_safe_writing, ()))
        self.q.put((self.do_safe_reading, ()))
        self.q.put((self.do_safe_reading, ()))
        self.q.join()

    def test_read_raises_exception(self):

        try:
            self.do_safe_reading_fail()
            self.assertTrue(False)
        except:
            pass

        self.assertEqual(self.writers, 0)
        self.assertEqual(self.readers, 0)

    def test_read_than_writes(self):

        self.q.put((self.do_safe_reading, ()))
        self.q.put((self.do_safe_reading, ()))
        self.q.put((self.do_safe_writing, ()))
        self.q.put((self.do_safe_writing, ()))
        self.q.join()

    def test_write(self):

        self.do_safe_writing()

        self.assertEqual(self.writers, 0)
        self.assertEqual(self.readers, 0)

    def test_write_raises_exception(self):

        try:
            self.do_safe_writing_fail()
            self.assertTrue(False)
        except:
            pass

        self.assertEqual(self.writers, 0)
        self.assertEqual(self.readers, 0)

    def test_mix(self):

        self.q.put((self.do_safe_reading, ()))
        self.q.put((self.do_safe_writing, ()))
        self.q.put((self.do_safe_reading, ()))
        self.q.put((self.do_safe_writing, ()))
        self.q.put((self.do_safe_reading, ()))
        self.q.put((self.do_safe_writing, ()))
        self.q.join()
