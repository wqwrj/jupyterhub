import os
from os.path import join

from pytablewriter import MarkdownTableWriter
from pytablewriter.style import Style

import jupyterhub.metrics

HERE = os.path.abspath(os.path.dirname(__file__))


class Generator:
    @classmethod
    def create_writer(cls, table_name, headers, values):
        writer = MarkdownTableWriter()
        writer.table_name = table_name
        writer.headers = headers
        writer.value_matrix = values
        writer.margin = 1
        [writer.set_style(header, Style(align="center")) for header in headers]
        return writer

    def _parse_metrics(self):
        table_rows = []
        for name in dir(jupyterhub.metrics):
            obj = getattr(jupyterhub.metrics, name)
            if obj.__class__.__module__.startswith('prometheus_client.'):
                for metric in obj.describe():
                    table_rows.append([metric.type, metric.name, metric.documentation])
        return table_rows

    def prometheus_metrics(self):
        generated_directory = f"{HERE}/source/monitoring/_gen"
        if not os.path.exists(generated_directory):
            os.makedirs(generated_directory)

        filename = f"{generated_directory}/metrics.md"
        table_name = "List of Prometheus Metrics"
        headers = ["Type", "Name", "Description"]
        values = self._parse_metrics()
        writer = self.create_writer(table_name, headers, values)
        with open(filename, 'w') as f:
            f.write(writer.dumps())


def main():
    doc_generator = Generator()
    doc_generator.prometheus_metrics()


if __name__ == "__main__":
    main()
