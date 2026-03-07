package com.nbo.crm.dto;

import lombok.Data;
import java.util.List;

@Data
public class NboResponse {
    // Maps JSON response containing recommended products
    private List<String> recommendations;
}