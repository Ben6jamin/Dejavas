#!/usr/bin/env python3

print("Testing imports...")

try:
    print("1. Testing FastAPI import...")
    from fastapi import FastAPI, HTTPException
    print("   ✓ FastAPI import successful")
except Exception as e:
    print(f"   ✗ FastAPI import failed: {e}")

try:
    print("2. Testing pydantic import...")
    from pydantic import BaseModel
    print("   ✓ Pydantic import successful")
except Exception as e:
    print(f"   ✗ Pydantic import failed: {e}")

try:
    print("3. Testing langgraph_simulation import...")
    from langgraph_simulation import LangGraphSimulator
    print("   ✓ LangGraphSimulator import successful")
except Exception as e:
    print(f"   ✗ LangGraphSimulator import failed: {e}")

try:
    print("4. Testing integrations import...")
    from integrations import IntegrationManager, IntegrationType, BrowserExtensionAPI, ScannedContent, ContentType
    print("   ✓ Integrations import successful")
except Exception as e:
    print(f"   ✗ Integrations import failed: {e}")

try:
    print("5. Testing agents import...")
    from agents import Agent, AgentFactory, AgentGenome
    print("   ✓ Agents import successful")
except Exception as e:
    print(f"   ✗ Agents import failed: {e}")

try:
    print("6. Testing simulation import...")
    from simulation import AdvancedSimulator, NetworkTopology
    print("   ✓ Simulation import successful")
except Exception as e:
    print(f"   ✗ Simulation import failed: {e}")

print("\nAll import tests completed!")
