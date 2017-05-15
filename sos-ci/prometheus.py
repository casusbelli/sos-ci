import os
import tempfile
import time


class PrometheusExporter():

    _export_dir = None
    _ci_name = None

    def __init__(self, exp_dir=None, ci_name="sos-ci"):
        if exp_dir:
            self._export_dir = exp_dir
        else:
            raise OSError(2, 'No export dir provided')

        self._ci_name = ci_name
        print("Initialized PrometheusExporter with ci_name: %(name)s and "
              "export directory: %(dir)s".format({"name": self._ci_name,
                                                  "dir": self._export_dir}))

    def export_queue_length(self, length=0):
        """exports the given length for the prometheus node_exporter"""
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        right_now = int(round(time.time()*1000,0))
        tmp_file.write(
            "sos_ci_queue_length {ci_name=\"" + self._ci_name
            + "\"} %(length)s %(time)s \n"
            .format({"length": length, "time": str(right_now)}))
        tmp_file.flush()
        os.fsync(tmp_file.fileno())
        tmp_file.close()
        os.chmod(tmp_file.name, 0666)
        print("moving export file from " + tmp_file.name + " to "
              + os.path.join(self._export_dir, self._ci_name + ".prom"))
        os.rename(tmp_file.name,
                  os.path.join(self._export_dir, self._ci_name + ".prom"))