#pragma once

#include "CoreMinimal.h"

class FUETestProject : public FDefaultGameModuleImpl
{
public:
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};