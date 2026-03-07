package com.nbo.crm.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

@Data
@Entity
@Table(name = "households")
public class Household {
    // Maps customer demographic data from PostgreSQL
    
    @Id
    @Column(name = "household_key")
    private Long householdKey;
    
    @Column(name = "age_desc")
    private String ageDesc;
    
    @Column(name = "marital_status_code")
    private String maritalStatusCode;
    
    @Column(name = "income_desc")
    private String incomeDesc;
    
    @Column(name = "homeowner_desc")
    private String homeownerDesc;
    
    @Column(name = "hh_comp_desc")
    private String hhCompDesc;
    
    @Column(name = "household_size_desc")
    private String householdSizeDesc;
    
    @Column(name = "kid_category_desc")
    private String kidCategoryDesc;
}