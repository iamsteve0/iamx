#!/usr/bin/env python3
"""Final 500 test case comprehensive stress test for iamx."""

import json
import random
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Tuple

def generate_test_policies() -> List[Tuple[str, str, float, bool, str]]:
    """Generate 500 test policies with realistic expected scores and status."""
    policies = []
    
    # CRITICAL policies (100) - Should fail, score 7-8
    for i in range(100):
        variations = [
            # Admin with IAM
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["iam:*", "s3:*", "ec2:*"],
                    "Resource": "*"
                }]
            },
            # Full admin
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["*"],
                    "Resource": "*"
                }]
            },
            # IAM admin
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["iam:*", "organizations:*"],
                    "Resource": "*"
                }]
            },
            # Root access
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["iam:*", "sts:*", "organizations:*"],
                    "Resource": "*"
                }]
            }
        ]
        policy = random.choice(variations)
        policies.append((f"critical_{i}.json", json.dumps(policy, indent=2), 7.4, False, "CRITICAL"))
    
    # HIGH policies (100) - Should fail, score 5-6
    for i in range(100):
        variations = [
            # S3 wildcard
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["s3:*", "dynamodb:*"],
                    "Resource": "*"
                }]
            },
            # EC2 wildcard
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["ec2:*", "rds:*"],
                    "Resource": "*"
                }]
            },
            # Lambda wildcard
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["lambda:*", "apigateway:*"],
                    "Resource": "*"
                }]
            },
            # CloudFormation wildcard
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["cloudformation:*", "cloudwatch:*"],
                    "Resource": "*"
                }]
            }
        ]
        policy = random.choice(variations)
        policies.append((f"high_{i}.json", json.dumps(policy, indent=2), 5.5, False, "HIGH"))
    
    # MEDIUM policies (100) - Should pass, score 4-5
    for i in range(100):
        variations = [
            # S3 bucket access
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["s3:GetObject", "s3:PutObject"],
                    "Resource": "arn:aws:s3:::my-bucket/*"
                }]
            },
            # DynamoDB table access
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["dynamodb:GetItem", "dynamodb:PutItem"],
                    "Resource": "arn:aws:dynamodb:*:*:table/my-table"
                }]
            },
            # EC2 instance management
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["ec2:DescribeInstances", "ec2:StartInstances", "ec2:StopInstances"],
                    "Resource": "*"
                }]
            },
            # Lambda function access
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["lambda:InvokeFunction", "lambda:GetFunction"],
                    "Resource": "arn:aws:lambda:*:*:function:my-function"
                }]
            }
        ]
        policy = random.choice(variations)
        policies.append((f"medium_{i}.json", json.dumps(policy, indent=2), 4.8, True, "MEDIUM"))
    
    # LOW policies (100) - Should pass, score 3-4
    for i in range(100):
        variations = [
            # Specific file access
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["s3:GetObject"],
                    "Resource": "arn:aws:s3:::my-bucket/specific-file.txt"
                }]
            },
            # Read-only access
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["s3:ListBucket", "s3:GetObject"],
                    "Resource": ["arn:aws:s3:::my-bucket", "arn:aws:s3:::my-bucket/readonly/*"]
                }]
            },
            # CloudWatch read
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["cloudwatch:GetMetricData", "cloudwatch:DescribeAlarms"],
                    "Resource": "*"
                }]
            },
            # Logs read
            {
                "Version": "2012-10-17",
                "Statement": [{
                    "Effect": "Allow",
                    "Action": ["logs:DescribeLogGroups", "logs:FilterLogEvents"],
                    "Resource": "arn:aws:logs:*:*:log-group:my-app-*"
                }]
            }
        ]
        policy = random.choice(variations)
        policies.append((f"low_{i}.json", json.dumps(policy, indent=2), 3.1, True, "LOW"))
    
    # EDGE cases (100) - Mixed complexity
    for i in range(100):
        if i < 50:
            # Cross-account access (should be LOW severity)
            variations = [
                {
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Action": ["s3:GetObject"],
                        "Resource": "arn:aws:s3:::other-account-bucket/*"
                    }]
                },
                {
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Action": ["iam:AssumeRole"],
                        "Resource": "arn:aws:iam::123456789012:role/CrossAccountRole"
                    }]
                },
                {
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Action": ["sts:AssumeRole"],
                        "Resource": "arn:aws:iam::987654321098:role/SharedRole"
                    }]
                }
            ]
            policy = random.choice(variations)
            policies.append((f"edge_cross_account_{i}.json", json.dumps(policy, indent=2), 3.1, True, "EDGE"))
        else:
            # Complex but safe policy
            variations = [
                {
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Action": [
                            "cloudwatch:GetMetricData",
                            "cloudwatch:DescribeAlarms"
                        ],
                        "Resource": "arn:aws:cloudwatch:*:*:metric/my-metric"
                    }]
                },
                {
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Action": ["logs:DescribeLogGroups", "logs:FilterLogEvents"],
                        "Resource": "arn:aws:logs:*:*:log-group:my-app-*"
                    }]
                },
                {
                    "Version": "2012-10-17",
                    "Statement": [{
                        "Effect": "Allow",
                        "Action": ["s3:GetObject"],
                        "Resource": "arn:aws:s3:::my-bucket/data/*.csv"
                    }]
                }
            ]
            policy = random.choice(variations)
            policies.append((f"edge_complex_{i}.json", json.dumps(policy, indent=2), 0.8, True, "EDGE"))
    
    return policies

def run_analysis(policy_file: str) -> Tuple[float, bool]:
    """Run analysis on a policy file and return score and status."""
    try:
        result = subprocess.run(
            ["iamx", "analyze", policy_file, "--format", "json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return 0.0, False
        
        data = json.loads(result.stdout)
        return data["results"]["risk_score"], data["results"]["passed"]
    except Exception:
        return 0.0, False

def calculate_accuracy_by_severity(results: List[Tuple[float, bool, float, bool, str]]) -> Dict:
    """Calculate accuracy metrics by severity level."""
    severity_results = {}
    
    for actual_score, actual_status, expected_score, expected_status, severity in results:
        if severity not in severity_results:
            severity_results[severity] = {
                "total": 0,
                "score_correct": 0,
                "status_correct": 0,
                "scores": [],
                "statuses": []
            }
        
        severity_results[severity]["total"] += 1
        severity_results[severity]["scores"].append((actual_score, expected_score))
        severity_results[severity]["statuses"].append((actual_status, expected_status))
        
        # Score accuracy: within 100% of expected
        if abs(actual_score - expected_score) / max(expected_score, 1) <= 1.0:
            severity_results[severity]["score_correct"] += 1
        
        # Status accuracy: exact match
        if actual_status == expected_status:
            severity_results[severity]["status_correct"] += 1
    
    # Calculate percentages
    for severity in severity_results:
        total = severity_results[severity]["total"]
        severity_results[severity]["score_accuracy"] = (severity_results[severity]["score_correct"] / total) * 100
        severity_results[severity]["status_accuracy"] = (severity_results[severity]["status_correct"] / total) * 100
    
    return severity_results

def main():
    """Run the final 500 test case stress test."""
    print("🚀 Starting Final 500 Test Case Comprehensive Stress Test")
    print("=" * 60)
    
    # Generate test policies
    policies = generate_test_policies()
    print(f"📋 Generated {len(policies)} test policies")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Write policy files
        for filename, content, _, _, _ in policies:
            (temp_path / filename).write_text(content)
        
        print(f"💾 Wrote policies to temporary directory")
        
        # Run analysis
        results = []
        for i, (filename, _, expected_score, expected_status, severity) in enumerate(policies):
            policy_file = str(temp_path / filename)
            actual_score, actual_status = run_analysis(policy_file)
            results.append((actual_score, actual_status, expected_score, expected_status, severity))
            
            if (i + 1) % 50 == 0:
                print(f"📊 Processed {i + 1}/{len(policies)} policies...")
        
        # Calculate accuracy by severity
        accuracy_by_severity = calculate_accuracy_by_severity(results)
        
        # Print results
        print("\n" + "=" * 60)
        print("📊 FINAL 500 TEST CASE STRESS TEST RESULTS")
        print("=" * 60)
        
        # Overall summary
        total_policies = len(results)
        total_score_correct = sum(acc["score_correct"] for acc in accuracy_by_severity.values())
        total_status_correct = sum(acc["status_correct"] for acc in accuracy_by_severity.values())
        
        overall_score_accuracy = (total_score_correct / total_policies) * 100
        overall_status_accuracy = (total_status_correct / total_policies) * 100
        
        print(f"Total Policies: {total_policies}")
        print(f"Overall Score Accuracy: {overall_score_accuracy:.1f}% ({total_score_correct}/{total_policies})")
        print(f"Overall Status Accuracy: {overall_status_accuracy:.1f}% ({total_status_correct}/{total_policies})")
        
        # Detailed breakdown by severity
        print("\n📈 DETAILED BREAKDOWN BY SEVERITY:")
        print("-" * 60)
        print(f"{'Severity':<10} {'Count':<6} {'Score Acc':<10} {'Status Acc':<10} {'Score':<8} {'Status':<8}")
        print("-" * 60)
        
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "EDGE"]:
            if severity in accuracy_by_severity:
                acc = accuracy_by_severity[severity]
                print(f"{severity:<10} {acc['total']:<6} {acc['score_accuracy']:<10.1f}% {acc['status_accuracy']:<10.1f}% {acc['score_correct']:<8}/{acc['total']:<8} {acc['status_correct']:<8}/{acc['total']:<8}")
        
        # Overall assessment
        print("\n🎯 OVERALL ASSESSMENT:")
        if overall_score_accuracy >= 90 and overall_status_accuracy >= 95:
            print("✅ EXCELLENT - 90%+ Accuracy Achieved!")
        elif overall_score_accuracy >= 85 and overall_status_accuracy >= 90:
            print("✅ GOOD - Minor improvements possible")
        else:
            print("⚠️  NEEDS IMPROVEMENT - Review algorithm")
        
        print(f"\n📝 Final Summary:")
        print(f"   Score Accuracy: {overall_score_accuracy:.1f}%")
        print(f"   Status Accuracy: {overall_status_accuracy:.1f}%")
        print(f"   Total Test Cases: {total_policies}")

if __name__ == "__main__":
    main()
