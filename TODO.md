# TODO

## Add Library Support
```
	<properties>
		<org.jenkinsci.plugins.workflow.libs.FolderLibraries plugin="workflow-cps-global-lib@2.8">
      <libraries>
        <org.jenkinsci.plugins.workflow.libs.LibraryConfiguration>
          <name>test</name>
          <retriever class="org.jenkinsci.plugins.workflow.libs.SCMSourceRetriever">
            <scm class="org.jenkinsci.plugins.github_branch_source.GitHubSCMSource" plugin="github-branch-source@2.0.4">
              <id>30d7f79a-88ad-4669-ce52-58611c6be770</id>
              <checkoutCredentialsId>SAME</checkoutCredentialsId>
              <scanCredentialsId>...</scanCredentialsId>
              <repoOwner>...</repoOwner>
              <repository>...</repository>
              <includes>*</includes>
              <excludes></excludes>
              <buildOriginBranch>true</buildOriginBranch>
              <buildOriginBranchWithPR>true</buildOriginBranchWithPR>
              <buildOriginPRMerge>false</buildOriginPRMerge>
              <buildOriginPRHead>false</buildOriginPRHead>
              <buildForkPRMerge>true</buildForkPRMerge>
              <buildForkPRHead>false</buildForkPRHead>
            </scm>
          </retriever>
          <defaultVersion>master</defaultVersion>
          <implicit>true</implicit>
          <allowVersionOverride>true</allowVersionOverride>
        </org.jenkinsci.plugins.workflow.libs.LibraryConfiguration>
      </libraries>
    </org.jenkinsci.plugins.workflow.libs.FolderLibraries>
	</properties>
```
