#!/usr/bin/env python
"""Solution for SWICloud SRE Interview tasks

Author: Vladimir Germanov
Version: v0.1
Dashboard: https://my.appoptics.com/s/public/zlh14ff2h
"""


from solution.swi_cloud_sre import SwiCloudSreSolution


def main():
    """Main function
    """
    my_solution = SwiCloudSreSolution()
    metrics = my_solution.create_metrics()
    my_solution.upload_metrics(metrics)


if __name__ == "__main__":
    main()
