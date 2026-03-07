package com.nbo.crm.dto;

import com.nbo.crm.entity.Household;
import lombok.Data;
import java.util.Map;

@Data
public class CustomerProfileDto {    
    private Household demographics;
    private Integer segment;
    private Map<String, Double> rfmMetrics;
}