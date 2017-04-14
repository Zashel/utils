import unittest
from multiprocessing import Pipe
from multiprocessing.connection import PipeConnection
from threading import Thread
from zashel.utils import threadize, daemonize, asynchronic, log
from time import sleep


@log
@threadize
def fake_thread(pipein):
    data = pipein.recv()


@log
@daemonize
def fake_daemon():
    while True:
        sleep(1)


@log
@asynchronic
def fake_asynchron(pipein):
    data = pipein.recv()
    return data


class Test(unittest.TestCase):
    def test_0_threadize(self):
        pipein, pipeout = Pipe(False)
        thread = fake_thread(pipein)
        self.assertEqual(thread.__class__, Thread)
        self.assertEqual(thread.__name__, "fake_thread")
        self.assertEqual(fake_thread.__name__, "fake_thread")
        pipeout.send(0)

    def test_1_daemonize(self):
        daemon = fake_daemon()
        self.assertEqual(daemon.__class__, Thread)
        self.assertEqual(daemon.__name__, "fake_daemon")
        self.assertEqual(fake_daemon.__name__, "fake_daemon")
        self.assertTrue(daemon.daemon)

    def test_2_asynchronic(self):
        data = "Hello World!"
        pipein, pipeout = Pipe(False)
        asynchron = fake_asynchron(pipein)
        self.assertEqual(asynchron.__class__, PipeConnection)
        self.assertEqual(asynchron.__name__, "fake_asynchron")
        self.assertEqual(fake_asynchron.__name__, "fake_asynchron")
        pipeout.send(data)
        self.assertEqual(asynchron.recv(), data)


if __name__ == "__main__":
    unittest.main()