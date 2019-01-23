"""SWI Cloud Sre solution module
"""

import json
import fileinput
import os
from argparse import ArgumentParser
import appoptics_metrics


def count_average(json_data):
    """Counts the average response times of
    the individual and all probes targets
    (sample_ms is the response time)
    ITA: individual targets' averages
    STA: sum average of all targets

    return: list
    """
    sum_values = 0 #STA
    count_values = 0 #STA
    sum_target = dict() #ITA
    count_target = dict() #ITA
    average_target = dict() #ITA
    result = list()

    for moment in json_data:
        for i in json_data[moment]:
            sum_values += i['sample_ms'] #STA
            sum_target.setdefault(i['target'], 0) #ITA
            sum_target[i['target']] += i['sample_ms'] #ITA
            count_values += 1 #STA
            count_target.setdefault(i['target'], 0) #ITA
            count_target[i['target']] += 1 #ITA
    average = sum_values / count_values #STA
    data = {
        "name": "average.response.time.per.hour",
        "value": str(average)
    } #STA
    result.append(data)

    for target in sum_target:
        average_target[target] = sum_target[target] / count_target[target]
        data = {
            "name": str("average.response.time.per.hour." + target),
            "value": str(average_target[target])
        } #ITA
        result.append(data)

    return result


def probes_per_minute(json_data):
    """Counts probes per minute.

    Return: list
    """
    result = list()
    for minute in json_data:
        data = {
            "name": "probes.per.minute",
            "value": str(len(json_data[minute])),
            "time": minute
        }
        result.append(data)

    return result


def longest_probe(json_data):
    """Determines the maximum probe time for each source.
    (sample_ms is the response time)

    Return: list
    """
    probes = dict()
    maxprobe = dict()
    result = list()

    for moment in json_data:
        for i in json_data[moment]:
            source = i['source']
            probelength = i['sample_ms']
            probes.setdefault(source, []).append(probelength)
            maxprobe[source] = max(probes[source])

    for source in maxprobe:
        data = {
            "name": str("longest.probe." + source),
            "value": str(maxprobe[source])
        }
        result.append(data)

    return result


def get_version():
    """Get the version of the app.

    Return: str
    """
    __version__ = ""
    try:
        with open(get_abs_path('../VERSION')) as version_file:
            __version__ = version_file.read().strip()
    except IOError:
        pass

    return __version__


def get_author():
    """Get the author of the app.

    Return: str
    """
    __author__ = ""
    try:
        with open(get_abs_path('../AUTHOR')) as author_file:
            __author__ = author_file.read().strip()
    except IOError:
        pass

    return __author__


def get_abs_path(file=None):
    """Return the absolute path of a file

    Return: str
    """
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), file)


class SwiCloudSreSolution(object):
    """SWI Cloud Sre solution base class.

    Usage:
    sol = SwiCloudSreSolution()
    metrics = sol.create_metrics()
    sol.upload_metrics(metrics)
    """
    def __init__(self):
        self._api_token = 'e7c96ca25fce8f452dbae662cbc70f1c3912b882c1bff9de26995ebe1821b86d'
        self._dashboard = 'https://my.appoptics.com/s/public/zlh14ff2h'


    def get_api_token(self):
        """Get the API authentication token

        Return: str
        """
        return self._api_token


    def set_api_token(self, token):
        """Set the API authentication token

        Return: str
        """
        self._api_token = token

        return self._api_token


    def get_dashboard(self):
        """Get the dashboard url

        Return: str
        """
        return self._dashboard


    def create_metrics(self):
        """Create metrics.

        Return: dict
        """
        json_data_input = ""
        result = dict()

        args = self.parse_args()

        for line in fileinput.input(files=os.path.abspath(args.files[0]) \
        if len(args.files) > 0 else ('-', )):
            json_data_input += line

        result['count_average'] = count_average(json.loads(json_data_input))
        result['probes_per_minute'] = probes_per_minute(json.loads(json_data_input))
        result['longest_probe'] = longest_probe(json.loads(json_data_input))

        return result


    def parse_args(self):
        """Parse cmd arguments

        Return: namespace
        """
        if get_version() and get_author():
            parser = ArgumentParser(
                description="Solution for SolarWinds Cloud SRE Interview Task, {}"
                .format(str(get_version())),
                epilog="Copyright 2019, {}, \
                        MIT (see LICENSE or https://opensource.org/licenses/MIT)"
                .format(str(get_author()))
            )
        elif get_version() and not get_author():
            parser = ArgumentParser(
                description="Solution for SolarWinds Cloud SRE Interview Task, {}"
                .format(str(get_version()))
            )
        elif not get_version() and get_author():
            parser = ArgumentParser(
                description="Solution for SolarWinds Cloud SRE Interview Task",
                epilog="Copyright 2019, {},\
                            MIT (see LICENSE or https://opensource.org/licenses/MIT)"
                .format(str(get_author()))
            )
        else:
            parser = ArgumentParser(description="Solution for SolarWinds Cloud SRE Interview Task")

        parser.add_argument(
            'files',
            metavar='FILE',
            nargs='*',
            help='file to read, if empty, stdin is used'
        )
        parser.add_argument(
            '-t',
            '--api_token',
            dest='token',
            type=str,
            help='api authentication token, if empty, default is used'
        )
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s {}'.format(get_version())
        )

        args = parser.parse_args()

        if args.token:
            self.set_api_token(args.token)

        return args


    def upload_metrics(self, metrics=None):
        """Upload metrics to API address.
        """
        count_average_data = metrics['count_average']
        probes_per_minute_data = metrics['probes_per_minute']
        longest_probe_data = metrics['longest_probe']

        api = appoptics_metrics.connect(self.get_api_token())

        try:
            with api.new_queue(tags={'swicloud_sre_solution': 'vladimir_germanov'}) as queue:
                for data in count_average_data:
                    queue.add(data['name'], data['value'])
                for data in longest_probe_data:
                    queue.add(data['name'], data['value'])
                for data in probes_per_minute_data:
                    queue.add(data['name'], data['value'], data['time'])

            print("Metrics uploaded successfully! Check: {}".format(self.get_dashboard()))
        except appoptics_metrics.exceptions.Unauthorized as error:
            print("Authorization failed! Token: {} is not corret!".format(self.get_api_token()))
            print("Error code: {}".format(error))
        except appoptics_metrics.exceptions.Forbidden as error:
            print("Not allowed operation with TOKEN: {}!".format(self.get_api_token()))
            print("Error code: {}".format(error))
