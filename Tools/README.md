# WhaleSongs Tools

Please use the [table of contents](../README.md) located at the root if you wish to navigate Tools.

## Creating a Tool

Note: These instructions will be collapsed down at merge time; for now they are a lightly modified copy of the walkthroughs.

#### Step 1: Clone the WhaleSongs repository or pull it:
```shell
# Clone
$ git clone git@github.com:DockerSolutionsEngineering/WhaleSongs.git

# Pull
$ git checkout main
$ git pull --rebase origin main
```
#### Step 2: Create a feature branch
```shell
$ git checkout -b NameOfYourTool
```
#### Step 3: Create a new directory for your Tool and copy the contents of the Example folder to it:
```shell
$ cd ./WhaleSongs/Tools
$ mkdir NameOfYourTool
$ cp -R ./Example/. ../NameOfYourTool/.
```
#### Step 4: Open the root of the repository in the editor of your choice:
```shell
$ cd ..
$ ${your editor} .
```

#### Step 5: Add your Tool to the [table of contents](../README.md) in alphabetical order and with a relative link:

```
* [Walkthroughs](./Walkthroughs/)
   - [Enable Remote Logging with Splunk](/Walkthroughs/EnableRemoteLoggingWithSplunk/)
   - [Enabling Virtulization Framework on macOS](/Walkthroughs/EnablingVirtualizationOnMacOS/)
   - [Monitoring Docker Desktop with Grafana](./Walkthroughs/MonitoringWithGrafana/)
   - [Understanding Docker Logs](/Walkthroughs/UnderstandingDockerLogs/)
   - [Understanding Where Scout Sends Data](/Walkthroughs/ScoutDataTransmission/)
+  - [Title of Your Walkthrough](/Walkthroughs/NameOfYourWalkthrough/)
```

#### Step 6: Edit the README.md in your folder and follow the outline provided

#### Step 7: Push your feature branch and open a pull request
```shell
$ git add .
$ git commit -am "Add NameOfYourTool Tool"
$ git push origin NameOfYourWalkthrough
```
![PullRequestButton](./images/openpullrequest.png)

