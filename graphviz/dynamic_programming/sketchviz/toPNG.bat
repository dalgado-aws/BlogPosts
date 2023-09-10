set yamlFile=%1
cat %yamlFile%.dot | dot -Tpng > %yamlFile%.png


