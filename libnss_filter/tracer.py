from logger import log
import pandas as pd


class DataModel(object):
    # Inlude methods to operate json data and find flow
    def __init__(self, df: pd.DataFrame):
        self.lev = 0
        self.nodes, self.edges = pd.DataFrame(), pd.DataFrame()
        # Classify Objects with two categories by its `type`: Node and edge
        df = df.groupby(df.type)

        self.nodes = pd.concat(
            [df.get_group("Artifact"), df.get_group("Process")], ignore_index=True
        )
        self.edges = pd.concat(
            [
                df.get_group("Used"),
                df.get_group("WasGeneratedBy"),
                df.get_group("WasDerivedFrom"),
                df.get_group("WasTriggeredBy"),
            ],
            ignore_index=True,
        )

        # Drop all empty columns
        self.edges = self.edges.dropna(axis="columns", how="all")
        self.nodes = self.nodes.dropna(axis="columns", how="all")

        # Set index for better query
        log.debug(
            "`edges` has the following columns:\n%s"
            % self.edges.columns.values.tolist()
        )
        log.debug(
            "`nodes` has the following columns:\n%s"
            % self.nodes.columns.values.tolist()
        )

        self.edges = self.edges.set_index(["annotations.event id"])
        self.nodes = self.nodes.set_index(["id"])

        log.debug("Edges\n%s" % self.edges)
        log.debug("Nodes\n%s" % self.nodes)

        # Export for debug
        self.edges.to_csv("./edges.csv", sep=",", index=False, header=True)
        self.nodes.to_csv("./nodes.csv", sep=",", index=False, header=True)

    def query_atrifact_id(self, path):
        """
        To query atrifact in df by its path, return its id
        """
        return self.df.loc[self.df["annotations.path"] == path][0][
            "id"
        ]  # query result should be the one and only

    def trace_atrifacts_upwards(self, targetid, lev):
        """
        To trace which artifacts trigger target atrifact with specific id. May cause recursive call.
        @targetid: center entity wanna trace
        @lev: max levels wanna trace
        """
        self.lev = lev
