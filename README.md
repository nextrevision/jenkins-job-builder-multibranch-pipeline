# jenkins-job-builder-multibranch-pipeline

Support for [multibranch pipelines](https://plugins.jenkins.io/workflow-multibranch) in JJB.

## Installation

```
pip install git+https://github.com/nextrevision/jenkins-job-builder-multibranch-pipeline
```

## Examples

Minimal Job Configuration

```
- job:
    name: jenkins-job-builder-multibranch-pipeline
    project-type: multibranch-pipeline
    multibranch:
      scm:
        github:
          repo: 'jenkins-job-builder-multibranch-pipeline'
          repo-owner: 'nextrevision'
```

Complete Configuration

```
- job:
    name: jenkins-job-builder-multibranch-pipeline
    project-type: multibranch-pipeline
    multibranch:
      num-to-keep: '200'
      days-to-keep: '100'
      prune-dead-branches: false
      healthmetrics-nonrecursive: true
      docker-label: '17.04'
      registry:
        url: https://my.dockerregistry.com
        credentials-id: '07f96af2-a52c-4144-ae5b-deb4f7b31fa3'
      triggers:
        spec: 'H H * * *'
        interval: '280000'
      scm:
        github:
          repo: 'jenkins-job-builder-multibranch-pipeline'
          repo-owner: 'nextrevision'
          scan-credentials-id: '0b6eebc5-a630-43e3-a9e5-a7407213cb82'
          checkout-credentials-id: 'f5d551d6-f479-4f9c-b8fa-17eb3f70b4f8'
          includes: 'feature/*'
          excludes: 'master'
          build-origin-branch: false
          build-origin-branch-with-pr: false
          build-origin-pr-merge: true
          build-origin-pr-head: true
          build-fork-pr-merge: false
          build-fork-pr-head: true
```
