package com.nbo.crm.controller;

import com.nbo.crm.dto.CustomerProfileDto;
import com.nbo.crm.dto.NboResponse;
import com.nbo.crm.service.AiModelService;
import com.nbo.crm.service.CustomerProfileService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/customers")
@CrossOrigin(origins = "http://localhost:4200")
public class CustomerController {

    private final CustomerProfileService customerProfileService;
    private final AiModelService aiModelService;

    public CustomerController(CustomerProfileService customerProfileService, AiModelService aiModelService) {
        this.customerProfileService = customerProfileService;
        this.aiModelService = aiModelService;
    }

    // Exposes the Customer 360 profile to the frontend
    @GetMapping("/{id}/profile")
    public ResponseEntity<CustomerProfileDto> getCustomerProfile(@PathVariable Long id) {
        CustomerProfileDto profile = customerProfileService.getCustomer360Profile(id);
        return ResponseEntity.ok(profile);
    }

    // Exposes the NBO recommendation engine to the frontend
    @PostMapping("/recommendations")
    public ResponseEntity<NboResponse> getRecommendations(@RequestBody List<String> currentBasket) {
        NboResponse recommendations = aiModelService.getNextBestOffer(currentBasket);
        return ResponseEntity.ok(recommendations);
    }
}