import sys
import time
import json


from splunklib.searchcommands import dispatch, GeneratingCommand, Option, Configuration
import virustotal3


class VirusTotalSearchCommand(GeneratingCommand):
    """A custom search command that returns the results of a VirusTotal search"""

    q = Option(require=True)

    def generate(self):
        api_key = "cd979b1284d8186ded168794d875ebb224e4420e01c68b971bb9aa4e0f0a6496"

        virus_total = virustotal3.core.IP(api_key)

        try:
            result = virus_total.info_ip(self.q)

            yield self.get_event(result["data"])

        except Exception as error:  # pylint: disable=broad-except
            self.get_event(
                {
                    "error": "No result from virustotal with error: "
                    + str(error)
                    + " for query: "
                    + self.q
                    + ""
                }
            )

    def get_event(self, result):
        """Return an event"""
        event = result
        event["_time"] = time.time()
        event["_raw"] = json.dumps(result)
        return event


dispatch(
    VirusTotalSearchCommand, sys.argv, sys.stdin, sys.stdout, __name__
)  # pylint: disable=abstract-class-instantiated
