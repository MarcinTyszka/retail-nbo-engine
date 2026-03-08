package com.nbo.crm.service;

import com.nbo.crm.dto.CustomerProfileDto;
import com.nbo.crm.dto.NboResponse;
import com.nbo.crm.dto.SegmentationResponse;
import com.nbo.crm.entity.Household;
import com.nbo.crm.repository.HouseholdRepository;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class CustomerProfileService {

    private final HouseholdRepository householdRepository;
    private final AiModelService aiModelService;

    public CustomerProfileService(HouseholdRepository householdRepository, AiModelService aiModelService) {
        this.householdRepository = householdRepository;
        this.aiModelService = aiModelService;
    }

public CustomerProfileDto getCustomer360Profile(Long householdKey) {
        Household household = householdRepository.findById(householdKey)
                .orElseThrow(() -> new RuntimeException("Customer not found: " + householdKey));

        SegmentationResponse aiResponse = aiModelService.getCustomerSegment(householdKey);
        List<String> lastBasket = householdRepository.findLastBasketByHousehold(householdKey);
        NboResponse nboResponse = aiModelService.getNextBestOffer(lastBasket);

        CustomerProfileDto profile = new CustomerProfileDto();
        profile.setDemographics(household);
        profile.setCurrentBasket(lastBasket);
        
        if (aiResponse != null) {
            profile.setSegment(aiResponse.getSegment());
            profile.setRfmMetrics(aiResponse.getMetrics());
        }
        
        if (nboResponse != null) {
            profile.setRecommendations(nboResponse.getRecommendations());
        }

        return profile;
    }
}