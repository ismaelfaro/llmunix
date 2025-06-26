# LLC Communication Templates
## Standard Message Templates for Common Agent Interactions

### Template Categories

This document provides standardized LLC message templates for common agent communication patterns in LLMunix. These templates ensure consistent, efficient communication while maintaining full context preservation.

## 1. Memory Query Templates

### Memory Analysis Request
```llc
@protocol: LLC/1.0
@from: SystemAgent
@to: MemoryAnalysisAgent
@priority: medium
@type: request

# Memory Query: {query_description}

Query memory for insights on {specific_topic} to inform current execution planning.

## Context Block
```context
domain: memory_analysis
task_type: query
confidence: 0.80
dependencies: []
resources: {
  memory_required: 64,
  cpu_intensive: false,
  external_apis: []
}
current_task_context: {current_goal}
query_urgency: medium
```

## Data Block
```data
{
  "query": "{natural_language_question}",
  "filters": {
    "outcome": null,
    "tags": [],
    "date_range": null,
    "sentiment": null,
    "components_used": []
  },
  "context": "{current_task_description}",
  "expected_insights": [
    "behavioral_recommendations",
    "component_selection_guidance",
    "error_prevention_strategies"
  ]
}
```

## Actions Block
```actions
- name: analyze_memory_patterns
  parameters: {
    depth: standard,
    include_behavioral_suggestions: true
  }
  expected_output: structured_analysis
  error_handling: continue_with_partial_results

- name: generate_recommendations
  parameters: {
    focus_areas: [constraints, components, error_prevention],
    confidence_threshold: 0.7
  }
  expected_output: actionable_suggestions
  error_handling: provide_general_guidance
```

@end
```

### Memory Analysis Response
```llc
@protocol: LLC/1.0
@from: MemoryAnalysisAgent
@to: SystemAgent
@priority: medium
@type: response

# Memory Analysis Results: {query_topic}

Analysis completed with {confidence_score}% confidence. Found {experience_count} relevant experiences with key behavioral insights.

## Context Block
```context
domain: memory_analysis
task_type: query
confidence: {confidence_score}
analysis_scope: {experience_count}_experiences
pattern_strength: {pattern_reliability}
```

## Response Block
```response
status: success
execution_time: {analysis_time_ms}
resource_usage: {
  tokens_used: {token_count},
  memory_peak: {memory_mb},
  external_calls: 0
}
result: {
  "analysis_summary": "{high_level_findings}",
  "relevant_experiences": ["{experience_ids}"],
  "key_insights": [
    "{insight_1}",
    "{insight_2}",
    "{insight_3}"
  ],
  "recommendations": [
    "{recommendation_1}",
    "{recommendation_2}"
  ],
  "behavioral_suggestions": {
    "constraint_adaptations": {
      "priority": "{recommended_priority}",
      "active_persona": "{recommended_persona}",
      "error_tolerance": "{recommended_tolerance}"
    },
    "component_preferences": ["{preferred_components}"]
  },
  "confidence_score": {confidence_percentage}
}
errors: []
```

@end
```

## 2. Web Content Analysis Templates

### Web Fetch Request
```llc
@protocol: LLC/1.0
@from: SystemAgent
@to: RealWebFetchTool
@priority: {priority_level}
@type: request

# Web Content Retrieval: {content_description}

Fetch and extract content from {url} for {analysis_purpose}.

## Context Block
```context
domain: web_content_acquisition
task_type: fetch
confidence: 0.85
dependencies: []
resources: {
  memory_required: 128,
  cpu_intensive: false,
  external_apis: ["target_website"]
}
content_type: {expected_content_type}
analysis_downstream: {next_processing_step}
```

## Data Block
```data
{
  "url": "{target_url}",
  "extraction_focus": "{content_focus}",
  "quality_requirements": {
    "completeness": "high",
    "accuracy": "required",
    "format_preservation": true
  },
  "error_handling": {
    "retry_attempts": 3,
    "timeout_seconds": 30,
    "fallback_strategy": "partial_content_acceptable"
  },
  "metadata": {
    "timestamp": "{current_timestamp}",
    "request_id": "{unique_id}"
  }
}
```

## Actions Block
```actions
- name: fetch_content
  parameters: {
    preserve_structure: true,
    extract_main_content: true,
    remove_navigation: true
  }
  expected_output: clean_text_content
  error_handling: retry_with_modified_parameters

- name: validate_content_quality
  parameters: {
    min_word_count: 100,
    check_completeness: true
  }
  expected_output: quality_assessment
  error_handling: flag_for_review
```

@end
```

## 3. Summarization Templates

### Summarization Request
```llc
@protocol: LLC/1.0
@from: SystemAgent
@to: RealSummarizationAgent
@priority: {priority_level}
@type: request

# Content Summarization: {content_source}

Generate structured summary of {content_description} with focus on {summary_focus}.

## Context Block
```context
domain: content_analysis
task_type: summarization
confidence: 0.90
dependencies: [content_acquisition_step]
resources: {
  memory_required: 256,
  cpu_intensive: true,
  external_apis: []
}
business_context: {business_objective}
audience: {target_audience}
urgency: {processing_urgency}
```

## Data Block
```data
{
  "input_source": "{file|url|text}",
  "input_path": "{content_location}",
  "output_format": "{json|markdown|plain}",
  "summary_length": "{brief|detailed|executive}",
  "focus_areas": [
    "{focus_area_1}",
    "{focus_area_2}"
  ],
  "quality_requirements": {
    "accuracy": "high",
    "conciseness": "balanced",
    "actionability": true
  },
  "metadata": {
    "content_type": "{article|report|documentation}",
    "expected_length": "{word_count_estimate}"
  }
}
```

## Actions Block
```actions
- name: analyze_content_structure
  parameters: {
    identify_key_sections: true,
    extract_main_themes: true
  }
  expected_output: content_analysis
  error_handling: continue_with_basic_analysis

- name: generate_summary
  parameters: {
    preserve_key_facts: true,
    include_confidence_scores: true,
    business_relevance_filter: true
  }
  expected_output: structured_summary
  error_handling: provide_partial_summary

- name: validate_summary_quality
  parameters: {
    completeness_check: true,
    accuracy_verification: true
  }
  expected_output: quality_metrics
  error_handling: flag_quality_issues
```

@end
```

## 4. Statistical Analysis Templates

### Analysis Request
```llc
@protocol: LLC/1.0
@from: DataCoordinatorAgent
@to: StatisticalAnalysisAgent
@priority: {priority_level}
@type: request

# Statistical Analysis: {analysis_type}

Perform {analysis_description} on {dataset_description} for {business_objective}.

## Context Block
```context
domain: data_analysis
task_type: statistical_analysis
confidence: {initial_confidence}
dependencies: [data_validation_step]
resources: {
  memory_required: {memory_estimate},
  cpu_intensive: true,
  external_apis: []
}
business_context: {business_goal}
analysis_urgency: {urgency_level}
interpretability_requirement: {interpretability_level}
```

## Data Block
```data
{
  "dataset_path": "{data_file_location}",
  "analysis_specifications": {
    "descriptive_analysis": {
      "variables": ["{variable_list}"],
      "include_distributions": {true|false},
      "outlier_handling": "{strategy}"
    },
    "correlation_analysis": {
      "method": "{pearson|spearman|kendall}",
      "significance_level": {alpha_value}
    },
    "clustering_analysis": {
      "algorithms": ["{algorithm_list}"],
      "k_range": [{min_k}, {max_k}],
      "features": ["{feature_list}"],
      "standardization": "{none|z_score|minmax}"
    }
  },
  "output_requirements": {
    "format": "json",
    "include_plots": {true|false},
    "confidence_intervals": {true|false},
    "business_interpretation": true
  }
}
```

## Actions Block
```actions
- name: validate_data_quality
  parameters: {
    completeness_threshold: {threshold},
    consistency_checks: true
  }
  expected_output: data_quality_report
  error_handling: {error_strategy}

- name: perform_descriptive_analysis
  parameters: {
    generate_summary_statistics: true,
    assess_distributions: {true|false}
  }
  expected_output: descriptive_statistics
  error_handling: continue_with_warnings

- name: execute_correlation_analysis
  parameters: {
    correlation_matrix: true,
    significance_testing: {true|false}
  }
  expected_output: correlation_results
  error_handling: use_robust_methods

- name: perform_clustering_analysis
  parameters: {
    optimize_cluster_number: true,
    evaluate_stability: {true|false}
  }
  expected_output: clustering_results
  error_handling: try_alternative_algorithms
```

@end
```

## 5. Error Handling Templates

### Error Notification
```llc
@protocol: LLC/1.0
@from: {failing_agent}
@to: SystemAgent
@priority: high
@type: notification

# Error Notification: {error_category}

{error_description} occurred during {operation_context}. Recovery options available.

## Context Block
```context
domain: error_management
task_type: error_notification
confidence: 1.0
dependencies: [failed_operation]
resources: {
  memory_required: 32,
  cpu_intensive: false,
  external_apis: []
}
error_severity: {critical|high|medium|low}
operation_context: {failed_task_description}
```

## Data Block
```data
{
  "error_details": {
    "error_code": "{error_identifier}",
    "error_message": "{detailed_error_description}",
    "operation_step": "{step_that_failed}",
    "input_context": "{relevant_input_data}",
    "stack_trace": "{technical_details}"
  },
  "recovery_options": [
    {
      "strategy": "{recovery_approach_1}",
      "confidence": {success_probability},
      "cost_estimate": "{resource_requirements}"
    }
  ],
  "partial_results": {
    "available": {true|false},
    "usability": "{assessment}",
    "data": "{partial_output_if_available}"
  }
}
```

## Actions Block
```actions
- name: assess_error_impact
  parameters: {
    evaluate_partial_results: true,
    determine_recovery_feasibility: true
  }
  expected_output: impact_assessment
  error_handling: escalate_to_human

- name: recommend_recovery_strategy
  parameters: {
    consider_cost_constraints: true,
    evaluate_success_probability: true
  }
  expected_output: recovery_plan
  error_handling: provide_minimal_guidance
```

@end
```

## 6. Progress Update Templates

### Progress Notification
```llc
@protocol: LLC/1.0
@from: {working_agent}
@to: SystemAgent
@priority: low
@type: notification

# Progress Update: {task_name}

{progress_description} - {completion_percentage}% complete, estimated {time_remaining} remaining.

## Context Block
```context
domain: task_monitoring
task_type: progress_update
confidence: {current_confidence}
dependencies: []
resources: {
  memory_required: 16,
  cpu_intensive: false,
  external_apis: []
}
task_phase: {current_phase}
overall_health: {green|yellow|red}
```

## Data Block
```data
{
  "progress_metrics": {
    "completion_percentage": {percentage},
    "steps_completed": {completed_count},
    "total_steps": {total_count},
    "estimated_time_remaining": "{time_estimate}",
    "resource_utilization": {
      "memory_usage": "{current_memory}",
      "processing_time": "{elapsed_time}",
      "cost_accrued": "{current_cost}"
    }
  },
  "current_phase": {
    "phase_name": "{phase_description}",
    "phase_status": "{in_progress|completed|error}",
    "key_activities": ["{activity_list}"]
  },
  "performance_indicators": {
    "quality_score": {quality_metric},
    "efficiency_rating": {efficiency_score},
    "error_count": {error_count}
  }
}
```

@end
```

## Template Usage Guidelines

### Customization Instructions
1. **Replace Placeholders**: All `{placeholder}` values should be replaced with actual values
2. **Adjust Priority**: Set priority based on task urgency and business impact
3. **Context Adaptation**: Modify context blocks to reflect actual task requirements
4. **Error Handling**: Customize error handling strategies based on task criticality
5. **Resource Estimation**: Provide realistic resource requirement estimates

### Best Practices
1. **Consistent Formatting**: Always maintain LLC protocol structure
2. **Complete Context**: Include sufficient context for autonomous processing
3. **Clear Expectations**: Specify expected outputs and success criteria
4. **Graceful Degradation**: Define fallback strategies for error scenarios
5. **Performance Tracking**: Include metrics for continuous improvement

### Template Selection Guide
- **Memory Queries**: Use when consulting historical experiences
- **Web Content**: Use for live content acquisition and processing
- **Summarization**: Use for content analysis and summary generation
- **Statistical Analysis**: Use for data processing and insights generation
- **Error Handling**: Use for structured error reporting and recovery
- **Progress Updates**: Use for long-running task monitoring