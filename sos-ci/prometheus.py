import os
import tempfile

import log


class PrometheusExporter():

    _export_dir = None
    _ci_name = None
    _metric_name_suffix = "_queue_length"
    _metric_name = None

    def __init__(self, exp_dir=None, ci_name="sos-ci", logger=None):
        if exp_dir:
            self._export_dir = exp_dir
        else:
            if logger:
                logger.warning("No prometheus export directory was provided,"
                               "not exporting...")
            return False

        self._ci_name = ci_name
        self._metric_name = self._ci_name.replace("-", "_") + "_"\
                            + self._metric_name_suffix
        if logger:
            logger.info("Initialized PrometheusExporter with ci_name: "
                        + self._ci_name + " and export directory: "
                        + self._export_dir)

    def export_queue_length(self, length=0):
        """exports the given length for the prometheus node_exporter"""
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        tmp_file.write("# HELP " + self._metric_name +
                       " The number of waiting jobs.\n")
        tmp_file.write("# TYPE " + self._metric_name + " gauge\n")
        tmp_file.write(self._metric_name + " {ci_name=\""
                       + self._ci_name + "\", } " + str(length) + "\n")
        tmp_file.flush()
        os.fsync(tmp_file.fileno())
        tmp_file.close()
        os.chmod(tmp_file.name, 0666)
        os.rename(tmp_file.name,
                  os.path.join(self._export_dir, self._ci_name + ".prom"))
