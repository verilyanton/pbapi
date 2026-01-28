#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { PbapiStack } from './pbapi-stack';
import {DEPLOY_ENVIRONMENT, STACK_PREFIX} from "./constants";

const app = new cdk.App();

// dev Stack
new PbapiStack(app, `${STACK_PREFIX}-${DEPLOY_ENVIRONMENT}`, {
  stackName: `${STACK_PREFIX}-${DEPLOY_ENVIRONMENT}`,
  env: {region: process.env.CDK_DEFAULT_REGION},
  tags: {env: DEPLOY_ENVIRONMENT},
});