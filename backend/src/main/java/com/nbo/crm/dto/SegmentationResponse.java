package com.nbo.crm.dto;

import lombok.Data;
import java.util.Map;

@Data
public class SegmentationResponse {
    // Maps JSON response from segmentation endpoint
    private Long household_key;
    private Integer segment;
    private Map<String, Double> metrics;
}