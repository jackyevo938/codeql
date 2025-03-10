function RegisterExtractorPack(id)
    local extractor = GetPlatformToolsDirectory() ..
                          'Semmle.Extraction.CSharp.Driver'
    if OperatingSystem == 'windows' then extractor = extractor .. '.exe' end
    local windowsMatchers = {
        CreatePatternMatcher({'^dotnet%.exe$'}, MatchCompilerName, extractor,
                             {prepend = {'--dotnetexec', '--cil'}}),
        CreatePatternMatcher({'^csc.*%.exe$'}, MatchCompilerName, extractor, {
            prepend = {'--compiler', '"${compiler}"', '--cil'}
        }),
        CreatePatternMatcher({'^fakes.*%.exe$', 'moles.*%.exe'},
                             MatchCompilerName, nil, {trace = false})
    }
    local posixMatchers = {
        CreatePatternMatcher({'^mcs%.exe$', '^csc%.exe$'}, MatchCompilerName,
                             extractor, {
            prepend = {'--compiler', '"${compiler}"', '--cil'}
        }),
        CreatePatternMatcher({'^mono', '^dotnet$'}, MatchCompilerName,
                             extractor, {prepend = {'--dotnetexec', '--cil'}}),
        function(compilerName, compilerPath, compilerArguments, _languageId)
            if MatchCompilerName('^msbuild$', compilerName, compilerPath,
                                 compilerArguments) or
                MatchCompilerName('^xbuild$', compilerName, compilerPath,
                                  compilerArguments) then
                return {
                    replace = true,
                    invocations = {
                        BuildExtractorInvocation(id, compilerPath, compilerPath,
                                                 compilerArguments, nil, {
                            '/p:UseSharedCompilation=false'
                        })
                    }
                }
            end
        end
    }
    if OperatingSystem == 'windows' then
        return windowsMatchers
    else
        return posixMatchers
    end

end

-- Return a list of minimum supported versions of the configuration file format
-- return one entry per supported major version.
function GetCompatibleVersions() return {'1.0.0'} end
