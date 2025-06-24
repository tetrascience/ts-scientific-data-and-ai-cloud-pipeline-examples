ts-cli publish --type task-script \
                --namespace private-{YOUR_ORG_SLUG} \
                --slug testing-taskscript \
                --version v0.1.0 \
                testing-taskscript \
                -c {AUTH_FOLDER}/{AUTH_FILE} \
                -f



ts-cli publish --type protocol \
                --namespace private-{YOUR_ORG_SLUG} \
                --slug testing-protocol \
                --version v0.1.0 \
                testing-protocol \
                -c {AUTH_FOLDER}/{AUTH_FILE} \
                -f


