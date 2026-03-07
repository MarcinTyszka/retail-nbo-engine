package com.nbo.crm.service;

import com.nbo.crm.dto.NboRequest;
import com.nbo.crm.dto.NboResponse;
import com.nbo.crm.dto.SegmentationResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import java.util.List;

@Service
public class AiModelService {
    
    private final RestTemplate restTemplate;
    private final String aiServiceUrl;

    public AiModelService(RestTemplate restTemplate, @Value("${nbo.ai.service.url}") String aiServiceUrl) {
        this.restTemplate = restTemplate;
        this.aiServiceUrl = aiServiceUrl;
    }

    // Fetches customer segment from FastAPI microservice
    public SegmentationResponse getCustomerSegment(Long householdKey) {
        String url = aiServiceUrl + "/api/segmentation/" + householdKey;
        return restTemplate.getForObject(url, SegmentationResponse.class);
    }

    // Fetches product recommendations based on current basket
    public NboResponse getNextBestOffer(List<String> basketItems) {
        String url = aiServiceUrl + "/api/nbo";
        NboRequest request = new NboRequest();
        request.setBasket_items(basketItems);
        return restTemplate.postForObject(url, request, NboResponse.class);
    }
}