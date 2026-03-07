package com.nbo.crm.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

@Data
@Entity
@Table(name = "products")
public class Product {
    // Maps product details for ML recommendations translation
    
    @Id
    @Column(name = "product_id")
    private Long productId;
    
    @Column(name = "department")
    private String department;
    
    @Column(name = "commodity_desc")
    private String commodityDesc;
    
    @Column(name = "sub_commodity_desc")
    private String subCommodityDesc;
    
    @Column(name = "brand")
    private String brand;
}