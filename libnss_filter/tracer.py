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
        # TODO: edges and nodes can be grouped into smaller groups have single type values to save space
        self.edges = self.edges.set_index(["annotations.event id"])
        self.nodes = self.nodes.set_index(["id"])

        log.debug("Edges\n%s" % self.edges)
        log.debug("Nodes\n%s" % self.nodes)

        # Export for debug
        self.edges.to_csv("./edges.csv", sep=",", index=False, header=True)
        self.nodes.to_csv("./nodes.csv", sep=",", index=False, header=True)

    def get_node_by_path(self, path: str) -> pd.DataFrame:
        """
        To query atrifact in nodes by its path
        """
        return self.nodes.query("`annotations.path`==@path")
        return self.nodes.loc[self.nodes["annotations.path"] == path][
            0
        ]  # query result should be the one and only
    # TODO: 查询还有很大问题
    def get_node_by_id(self, id: str) -> pd.DataFrame:
        """
        To query artifact in nodes by its id
        """
        return self.nodes.query("`id`==@id")
        return self.nodes.loc[self.nodes["id"] == id][
            0
        ]  # query result should be the one and only

    def trace_atrifacts_upwards_by_path(self, path: str,lev:int)->list[str]:
        """
        External interface.To trace which artifacts trigger target atrifact with specific path. Just query for path, get its id and pass it to `trace_atrifacts_upwards_by_id`.
        """
        artifact = self.get_node_by_path(path)
        log.debug(artifact)
        if not artifact.empty:
            return self.trace_atrifacts_upwards_by_id(artifact.iloc[0]['id'],lev)# TODO: 这里有问题
        else:
            log.fatal("No atrifact %s found. Check input file."%path)
            return None
        
        

    def trace_atrifacts_upwards_by_id(self, target_id: str, lev: int)->list[str]:
        """
        To trace which artifacts trigger target atrifact with specific id. May cause recursive call.
        Args:
        targetid:
            Center entity wanna trace
        lev:
            Max levels wanna trace
        """
        self.lev = lev
        # TODO: main entry of query
        target_ids = [target_id]
        while self.lev:
            target_ids = self.trace_route_recursively(target_ids)
            # TODO: show each layer nodes info
        return target_ids

    def get_parent_node_by_id(self, target_id: str) -> list[str]:
        """
        Simply find the parent node of the node with the id provided and the edge. May get multi edges which lead to multi parent nodes
        """
        target_edges = self.edges.query("to==@target_id")
        # TODO: show each layer edges info

        return (
            target_edges["from"].drop_duplicates().values.tolist()
        )  # Drop dulicate records and return as a list

    def trace_route_recursively(self, target_id_group: list[str]) -> list[str]:
        """
        Recursive body to run query
        Args:
            target_id_group: list of node ids wanna trace
        Returns:
            list of nodes in the next level; can be recursed again
        """
        self.lev -= 1
        return list(set([self.get_parent_node_by_id(id) for id in target_id_group]))

    def show_record_info_by_id(self, isnode: bool, id: str) -> None:
        """
        Display node or edge with given id or event id
        For a node, the following info will be displayed:
            - type
            - pid namespace
            - annotations.net namespace
            - annotations.ipc namespace
            - annotations.ppid
            - annotations.pid namespace
            - annotations.exe
            - annotations.mount namespace
            - annotations.name
            - annotations.user namespace
            - annotations.path
            - annotations.subtype
            - annotations.command line
            - path
        For an edge, the following info will be displayed:
            - type
            - from
            - to
            - annotations.operation
        Args:
            isnode:
                true->nodes search by `id`
                false->edges search by `event id`

        """
        if isnode:
            result = self.get_node_by_id(id)
            # TODO: finish it later when the core functions are settled. display id and search it manually first.
