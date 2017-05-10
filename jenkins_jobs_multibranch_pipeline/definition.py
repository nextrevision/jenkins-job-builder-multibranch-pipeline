import logging
import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base
import uuid

from jenkins_jobs.errors import InvalidAttributeError
from jenkins_jobs.errors import MissingAttributeError

logger = logging.getLogger(str(__name__))


class WorkflowMultiBranch(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):
        xml_parent = XML.Element('org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject')
        xml_parent.attrib['plugin'] = 'workflow-multibranch'

        if 'multibranch' not in data:
            return xml_parent

        pdata = data['multibranch']

        XML.SubElement(xml_parent, 'actions')

        # properties
        properties = XML.SubElement(xml_parent, 'properties')

        # properties > folderConfig
        folderConfig = XML.SubElement(properties, 'org.jenkinsci.plugins.pipeline.modeldefinition.config.FolderConfig')
        folderConfig.attrib['plugin'] = 'pipeline-model-definition'
        XML.SubElement(folderConfig, 'dockerLabel').text = pdata.get('docker-label', '')

        # properties > folderConfig > registry
        registry = XML.SubElement(folderConfig, 'registry')
        registry.attrib['plugin'] = 'docker-commons'
        if 'registry' in pdata:
            XML.SubElement(registry, 'url').text = pdata['registry'].get('url', '')
            XML.SubElement(registry, 'credentialsId').text = pdata['registry'].get('credentials-id', '')

        # folderViews
        folderViews = XML.SubElement(xml_parent, 'folderViews')
        folderViews.attrib['class'] = 'jenkins.branch.MultiBranchProjectViewHolder'
        folderViews.attrib['plugin'] = 'branch-api'
        folderViewsOwner = XML.SubElement(folderViews, 'owner')
        folderViewsOwner.attrib['class'] = 'org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject'
        folderViewsOwner.attrib['reference'] = '../..'

        # healthMetrics
        healthMetrics = XML.SubElement(xml_parent, 'healthMetrics')
        healthMetricsWorstChild = XML.SubElement(healthMetrics, 'com.cloudbees.hudson.plugins.folder.health.WorstChildHealthMetric')
        healthMetricsWorstChild.attrib['plugin'] = 'cloudbees-folder'
        XML.SubElement(healthMetricsWorstChild, 'nonRecursive').text = str(pdata.get('healthmetrics-nonrecursive', 'false')).lower()

        # icon
        icon = XML.SubElement(xml_parent, 'icon')
        icon.attrib['class'] = 'jenkins.branch.MetadataActionFolderIcon'
        icon.attrib['plugin'] = 'branch-api'
        iconOwner = XML.SubElement(icon, 'owner')
        iconOwner.attrib['class'] = 'org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject'
        iconOwner.attrib['reference'] = '../..'

        # orphanedItemStrategy
        orphanedItemStrategy = XML.SubElement(xml_parent, 'orphanedItemStrategy')
        orphanedItemStrategy.attrib['class'] = 'com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy'
        orphanedItemStrategy.attrib['plugin'] = 'cloudbees-folder'
        XML.SubElement(orphanedItemStrategy, 'pruneDeadBranches').text = str(pdata.get('prune-dead-branches', 'true')).lower()
        XML.SubElement(orphanedItemStrategy, 'daysToKeep').text = pdata.get('days-to-keep', '-1')
        XML.SubElement(orphanedItemStrategy, 'numToKeep').text = pdata.get('num-to-keep', '-1')

        # triggers
        triggers = XML.SubElement(xml_parent, 'triggers')
        if 'triggers' in pdata:
            periodicFolderTrigger = XML.SubElement(triggers, 'com.cloudbees.hudson.plugins.folder.computed.PeriodicFolderTrigger')
            periodicFolderTrigger.attrib['plugin'] = 'cloudbees-folder'

            if 'spec' not in pdata['triggers']:
                raise MissingAttributeError('spec is required when specifying triggers')
            XML.SubElement(periodicFolderTrigger, 'spec').text = pdata['triggers']['spec']
            if 'interval' not in pdata['triggers']:
                raise MissingAttributeError('interval is required when specifying triggers')
            XML.SubElement(periodicFolderTrigger, 'interval').text = pdata['triggers']['interval']

        # sources
        if 'scm' in pdata:
            sources = XML.SubElement(xml_parent, 'sources')
            sources.attrib['class'] = 'jenkins.branch.MultiBranchProject$BranchSourceList'
            sources.attrib['plugin'] = 'branch-api'
            sourcesData = XML.SubElement(sources, 'data')
            branchSource = XML.SubElement(sourcesData, 'jenkins.branch.BranchSource')

            if 'github' in pdata['scm']:
                source = XML.SubElement(branchSource, 'source')
                source.attrib['class'] = 'org.jenkinsci.plugins.github_branch_source.GitHubSCMSource'
                source.attrib['plugin'] = 'github-branch-source'
                scm_data = pdata['scm']['github']

                if 'repo' not in scm_data:
                    raise MissingAttributeError('repo must be set in github scm')
                if 'repo-owner' not in scm_data:
                    raise MissingAttributeError('repo-owner must be set in github scm')

                XML.SubElement(source, 'id').text = str(uuid.uuid5(uuid.NAMESPACE_DNS, scm_data['repo-owner'] + '.' + scm_data['repo']))
                XML.SubElement(source, 'checkoutCredentialsId').text = scm_data.get('checkout-credentials-id', 'SAME')
                if 'scan-credentials-id' in scm_data:
                    XML.SubElement(source, 'scanCredentialsId').text = scm_data['scan-credentials-id']
                XML.SubElement(source, 'repoOwner').text = scm_data['repo-owner']
                XML.SubElement(source, 'repository').text = scm_data['repo']
                XML.SubElement(source, 'includes').text = scm_data.get('includes', '*')
                XML.SubElement(source, 'excludes').text = scm_data.get('excludes', '')
                XML.SubElement(source, 'buildOriginBranch').text = str(scm_data.get('build-origin-branch', 'true')).lower()
                XML.SubElement(source, 'buildOriginBranchWithPR').text = str(scm_data.get('build-origin-branch-with-pr', 'true')).lower()
                XML.SubElement(source, 'buildOriginPRMerge').text = str(scm_data.get('build-origin-pr-merge', 'false')).lower()
                XML.SubElement(source, 'buildOriginPRHead').text = str(scm_data.get('build-origin-pr-head', 'false')).lower()
                XML.SubElement(source, 'buildForkPRMerge').text = str(scm_data.get('build-fork-pr-merge', 'true')).lower()
                XML.SubElement(source, 'buildForkPRHead').text = str(scm_data.get('build-fork-pr-head', 'false')).lower()
            else:
                raise InvalidAttributeError("Unknown/unsupported scm type specified")

            # sources > branchSource > strategy
            strategy = XML.SubElement(branchSource, 'strategy')
            strategy.attrib['class'] = 'jenkins.branch.DefaultBranchPropertyStrategy'
            strategyProperties = XML.SubElement(strategy, 'properties')
            strategyProperties.attrib['class'] = 'empty-list'
            sourcesOwner = XML.SubElement(sources, 'owner')
            sourcesOwner.attrib['class'] = 'org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject'
            sourcesOwner.attrib['reference'] = '../..'

        # factory
        factory = XML.SubElement(xml_parent, 'factory')
        factory.attrib['class'] = 'org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory'
        factoryOwner = XML.SubElement(factory, 'owner')
        factoryOwner.attrib['class'] = 'org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject'
        factoryOwner.attrib['reference'] = '../..'

        return xml_parent
