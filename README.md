# better-puppet-graph
With this script you can prettify the `puppet --graph` output.

# usage
```sh
# get a graph
puppet test.pp --noop --graph --graphdir .
# transform
graph.py -c -i expanded_relationships.dot -o output.gefx
# open with gephi
gephi output.gefx
```

# example
