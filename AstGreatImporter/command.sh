#!/bin/bash
# if got error , clear the data quickly ! so cool !
#rm -rf ./neo4j-community-4.2.1/data/databases/neo4j/
# your neo4j path
./neo4j-community-4.2.1/bin/neo4j-admin import \
--database=neo4j \ 
--nodes=nodes.csv \
--relationships=rels.csv \
--relationships=cpg_edges.csv \
--trim-strings=true \
--skip-duplicate-nodes=true \
--skip-bad-relationships=true
