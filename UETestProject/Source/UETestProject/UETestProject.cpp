#include "UETestProject.h"
#include "Modules/ModuleManager.h"

#include "Internationalization/StringTableRegistry.h"


void FUETestProject::StartupModule()
{
	FDefaultGameModuleImpl::StartupModule();
	
	LOCTABLE_FROMFILE_GAME("Animals", "UETestProject", "Localization/StringTablesCSV/Animals.csv");
	LOCTABLE_FROMFILE_GAME("WbpTestTexts", "UETestProject", "Localization/StringTablesCSV/WbpTestTexts.csv");
}

void FUETestProject::ShutdownModule()
{
	FDefaultGameModuleImpl::ShutdownModule();
}

IMPLEMENT_PRIMARY_GAME_MODULE( FUETestProject, UETestProject, "UETestProject" );
