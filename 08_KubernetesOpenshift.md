### Step-by-Step Guide to Deploy Java Applications to Redhat Openshift(Kubernetes)

#### 1. Register for a RedHat Developer Sandbox
[https://developers.redhat.com/developer-sandbox](https://developers.redhat.com/developer-sandbox)

#### 2. Login to your RedHat Developer Sandbox
[https://developers.redhat.com/developer-sandbox/get-started](https://developers.redhat.com/developer-sandbox/get-started)
![oc](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/01_get_started_with_redhat_developer_sandbox.png)

#### 3. Install "oc" command line utility (RedHat's version of kubectl)
Instructions are [here](https://docs.openshift.com/container-platform/4.8/cli_reference/openshift_cli/getting-started-cli.html)

#### 4. Test "oc" command line utility
`oc status`
![oc](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/02_oc_status.png)

#### 5. Copy the "oc  login" command from the UI and run it on the console
![oc](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/03_copy_oc_login_command.png)
![oc](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/04_copy_oc_login_command.png)
![oc](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/05_copy_oc_login_command.png)

#### 6. Clone The Simple Java Application from GitHub
`git clone git@github.com:dalgado-aws/first-openshift-java.git`

#### 7. Change into Application Directory
`cd first-openshift-java`

#### 8. Create an "Image Stream" to refer to your Images
`oc create is my-java-image-stream`
![oc](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/07_create_image_stream.png)

#### 9. Create a "Build Config" to convert your Java Source Code to an Image
`oc apply -f manifests/oc_1_bc.yaml`
![oc](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/08_create_build_config.png)

#### 10. Start the Build to create an Image
`oc start-build build-my-java --from-dir=. --follow`
![oc](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/09_start_build_config.png)
![oc](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/10_start_build_config.png)

#### 11. Deploy the Image
`export OPENSHIFT_NAMESPACE=$(oc config view --minify -o 'jsonpath={..namespace}')`
`oc process -f manifests/oc_2_dc.yaml -p OPENSHIFT_NAMESPACE=$OPENSHIFT_NAMESPACE |oc create -f -`
![oc](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/11_deploy_build.png)

#### 12. Create the Service to access the application from within Openshift
`oc apply -f manifests/oc_3_service.yaml`
![oc](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/12_create_service.png)

#### 13. Create the Route to access the application from the Internet
`oc process -f manifests/oc_4_route.yaml -p OPENSHIFT_NAMESPACE=$OPENSHIFT_NAMESPACE |oc create -f - `
![oc](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/13_create_route.png)

#### 14. Access the Application
![oc](https://raw.githubusercontent.com/dalgado-aws/BlogPosts/master/img/openshift/14_access_route.png)
