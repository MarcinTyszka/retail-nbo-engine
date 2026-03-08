package com.nbo.crm.repository;

import com.nbo.crm.entity.Household;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface HouseholdRepository extends JpaRepository<Household, Long> {

    // query to fetch items from the customer most recent visit
    @Query(value = "SELECT p.sub_commodity_desc FROM transactions t " +
                   "JOIN products p ON t.product_id = p.product_id " +
                   "WHERE t.basket_id = (SELECT basket_id FROM transactions " +
                   "WHERE household_key = :householdKey ORDER BY day DESC LIMIT 1)", 
           nativeQuery = true)
    List<String> findLastBasketByHousehold(@Param("householdKey") Long householdKey);
}