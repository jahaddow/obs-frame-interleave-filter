cmake_minimum_required(VERSION 3.12)

project(obs-frame-interleave-filter VERSION 0.2.0)

set(PLUGIN_AUTHOR "Norihiro Kamae")

set(PLUGIN_URL "https://obsproject.com/forum/resources/obs-frame-interleave-filter.1618/")
set(ID_PREFIX "net.nagater.obs-frame-interleave-filter.")
set(MACOS_BUNDLEID "net.nagater.obs-frame-interleave-filter")
set(MACOS_PACKAGE_UUID "8FE719C3-6009-495D-AB7A-4DEC4D4DAD8F")
set(MACOS_INSTALLER_UUID "3FE71FAC-65AA-4078-90E3-E417E2AEF8DA")
set(WIN_INSTALLER_UUID   "BD8AB2DA-6DF3-4D5E-B26A-F984A691283F")

set(LINUX_MAINTAINER_EMAIL "norihiro@nagater.net")

option(ENABLE_COVERAGE "Enable coverage option for GCC" OFF)

if(${CMAKE_SOURCE_DIR} STREQUAL ${CMAKE_CURRENT_SOURCE_DIR})
	find_package(libobs REQUIRED)
	include(cmake/ObsPluginHelpers.cmake)
endif()

configure_file(
	src/plugin-macros.h.in
	plugin-macros.generated.h
)

set(PLUGIN_SOURCES
	src/plugin-main.c
	src/frame-interleave-filter.c
)

add_library(${PROJECT_NAME} MODULE ${PLUGIN_SOURCES})

target_link_libraries(${PROJECT_NAME}
	OBS::libobs
)

target_include_directories(${PROJECT_NAME}
	PRIVATE
	${CMAKE_CURRENT_BINARY_DIR}
)

if(OS_WINDOWS)
	# Enable Multicore Builds and disable FH4 (to not depend on VCRUNTIME140_1.DLL when building with VS2019)
	if (MSVC)
		add_definitions(/MP /d2FH4-)
	endif()

	target_link_libraries(${PROJECT_NAME} OBS::w32-pthreads)

	set(LICENSE_DESTINATION "data/obs-plugins/${PROJECT_NAME}")
endif()

if(OS_LINUX)
	target_compile_options(${PROJECT_NAME} PRIVATE -Wall -Wextra)
	target_link_options(${PROJECT_NAME} PRIVATE -Wl,-z,defs)

	set(LICENSE_DESTINATION ${CMAKE_INSTALL_DOCDIR})

	if(ENABLE_COVERAGE)
		target_compile_options(${PROJECT_NAME} PRIVATE -coverage -fprofile-update=atomic)
		target_link_options(${PROJECT_NAME} PRIVATE -coverage)
	endif()
endif()

if(APPLE)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -stdlib=libc++ -fvisibility=default")

	set(LICENSE_DESTINATION "${PROJECT_NAME}.plugin/Contents/Resources")

	set_target_properties(${PROJECT_NAME} PROPERTIES PREFIX "")
	set(MACOSX_PLUGIN_GUI_IDENTIFIER "${MACOS_BUNDLEID}")
	set(MACOSX_PLUGIN_BUNDLE_VERSION "${PROJECT_VERSION}")
	set(MACOSX_PLUGIN_SHORT_VERSION_STRING "1")
endif()

file(GENERATE OUTPUT .gitignore CONTENT "*\n")

if(CMAKE_C_COMPILER_ID STREQUAL GNU)
	target_compile_options(${PROJECT_NAME} PRIVATE -fanalyzer)
endif()

setup_plugin_target(${PROJECT_NAME})

option(INSTALL_LICENSE_FILES "Install license files" ON)
if(INSTALL_LICENSE_FILES)
	install(FILES
		LICENSE
		DESTINATION ${LICENSE_DESTINATION}
	)
endif()

if(${CMAKE_SOURCE_DIR} STREQUAL ${CMAKE_CURRENT_SOURCE_DIR})
	configure_file(
		installer/installer-Windows.iss.in
		installer-Windows.generated.iss
	)

	configure_file(
		ci/ci_includes.sh.in
		ci/ci_includes.generated.sh
	)
	configure_file(
		ci/ci_includes.cmd.in
		ci/ci_includes.generated.cmd
	)

	configure_file(
		installer/installer-macOS.pkgproj.in
		installer-macOS.generated.pkgproj
	)
endif()
