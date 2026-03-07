package com.nbo.crm.service;

import com.nbo.crm.dto.CustomerProfileDto;
import com.nbo.crm.dto.SegmentationResponse;
import com.nbo.crm.entity.Household;
import com.nbo.crm.repository.HouseholdRepository;
import org.springframework.stereotype.Service;

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

        CustomerProfileDto profile = new CustomerProfileDto();
        profile.setDemographics(household);
        
        if (aiResponse != null) {
            profile.setSegment(aiResponse.getSegment());
            profile.setRfmMetrics(aiResponse.getMetrics());
        }

        return profile;
    }
}