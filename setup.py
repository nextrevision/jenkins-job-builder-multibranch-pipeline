#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='jenkins-job-builder-multibranch-pipeline',
    version='0.1.2',
    description="Multi-Branch Pipeline support for jenkins-job-builder",
    author="John Patterson",
    url='https://github.com/nextrevision/jenkins-job-builder-multibranch-pipeline',
    packages=['jenkins_jobs_multibranch_pipeline'],
    include_package_data=True,
    install_requires=['jenkins-job-builder'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    entry_points={
        'jenkins_jobs.projects': [
            'multibranch-pipeline=jenkins_jobs_multibranch_pipeline.definition:WorkflowMultiBranch'
        ],
    },
)
