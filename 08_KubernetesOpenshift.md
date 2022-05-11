### Step-by-Step Guide to Deploy Java Applications to Redhat Openshift(Kubernetes)

#### 1. Create RedHat Developer Sandbox 
  - Register [https://developers.redhat.com/developer-sandbox](https://developers.redhat.com/developer-sandbox)
  - ![Register](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/01_get_started_with_redhat_developer_sandbox.png)
  - Login  [https://developers.redhat.com/developer-sandbox/get-started](https://developers.redhat.com/developer-sandbox/get-started)

#### 2. Install "oc" command line utility (RedHat's version of kubectl)
  - Instructions are [here](https://docs.openshift.com/container-platform/4.8/cli_reference/openshift_cli/getting-started-cli.html)
  - Once "oc" is installed, run `oc status` from the console. It should show an error message.

#### 3. Copy the "oc  login" command from the UI and run it on the console

#### 4. Clone the Simple Java Application from GitHub
  - `git clone git@github.com:dalgado-aws/first-openshift-java.git`

#### 5. Change into Application Directory
  - `cd first-openshift-java`

#### 6. Create an "Image Stream"
  - `oc create is my-java-image-stream`

#### 7. Create a "Build Config"
  - `oc apply -f manifests/oc_1_bc.yaml`

#### 8. Start the Build to create an Image
 - `oc start-build build-my-java --from-dir=. --follow`

#### 9. Deploy the Image
 - `export OPENSHIFT_NAMESPACE=$(oc config view --minify -o 'jsonpath={..namespace}')`
 - `oc process -f manifests/oc_2_dc.yaml -p OPENSHIFT_NAMESPACE=$OPENSHIFT_NAMESPACE |oc create -f -`

#### 10. Create the Service
  - `oc apply -f manifests/oc_3_service.yaml`

#### 12. Create the Route
  - `oc process -f manifests/oc_4_route.yaml -p OPENSHIFT_NAMESPACE=$OPENSHIFT_NAMESPACE |oc create -f - `