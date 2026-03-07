package com.nbo.crm.dto;

import lombok.Data;
import java.util.List;

@Data
public class NboRequest {
    // Maps JSON payload for sending basket items to ML model
    private List<String> basket_items;
}