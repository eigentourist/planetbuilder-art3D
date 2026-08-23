// Example Code Snippet
// Objective-C code from old codebase
// Built using Cocos2d-ObjectiveC
// Placed here for reference on how animated
// nebula background was assembled

        _bgSpectrum = [AnimatedBackground spriteWithImageNamed:@"ccbResources/Images/Clouds/spectrum.pvr.ccz"];
        _bgSpectrum.position = center;
        _bgSpectrum.zOrder = -6;
        _bgSpectrum.opacity = 1.0;
        _bgSpectrum.angleIncValue = BackgroundLayer0RotationIncrement;
        _bgSpectrum.clockwise = YES;
        _bgSpectrum.initialFrame = 0;
        _bgSpectrum.currentFrame = 0;
        _bgSpectrum.frameCount = 4;
        _bgSpectrum.layerName = @"Spectrum";

        _bgNoise1 = [AnimatedBackground spriteWithImageNamed:@"ccbResources/Images/Clouds/noise1.pvr.ccz"];
        _bgNoise1.position = center;
        _bgNoise1.zOrder = -5;
        _bgNoise1.opacity = 0.875;
        _bgNoise1.angleIncValue = BackgroundLayer1RotationIncrement;
        _bgNoise1.clockwise = NO;
        _bgNoise1.initialFrame = 1;
        _bgNoise1.currentFrame = 0;
        _bgNoise1.frameCount = 4;
        _bgNoise1.layerName = @"Noise1";

        _bgNoise2 = [AnimatedBackground spriteWithImageNamed:@"ccbResources/Images/Clouds/noise2.pvr.ccz"];
        _bgNoise2.position = center;
        _bgNoise2.zOrder = -4;
        _bgNoise2.opacity = 0.875;
        _bgNoise2.angleIncValue = BackgroundLayer2RotationIncrement;
        _bgNoise2.clockwise = YES;
        _bgNoise2.initialFrame = 2;
        _bgNoise2.currentFrame = 0;
        _bgNoise2.frameCount = 4;
        _bgNoise2.layerName = @"Noise2";

        _bgNoise3 = [AnimatedBackground spriteWithImageNamed:@"ccbResources/Images/Clouds/noise3.pvr.ccz"];
        _bgNoise3.position = center;
        _bgNoise3.zOrder = -3;
        _bgNoise3.opacity = 0.875;
        _bgNoise3.angleIncValue = BackgroundLayer2RotationIncrement;
        _bgNoise3.clockwise = NO;
        _bgNoise3.initialFrame = 3;
        _bgNoise3.currentFrame = 0;
        _bgNoise3.frameCount = 4;
        _bgNoise3.layerName = @"Noise3";

        // Blend Src: Dst Color   Blend Dst: One Minus Src Alpha

        CCBlendMode *lightBlend0 = [CCBlendMode blendModeWithOptions:@{
                                                                       CCBlendFuncSrcColor: @(GL_ONE),
                                                                       CCBlendFuncDstColor: @(GL_ONE),
                                                                       }];
        CCBlendMode *lightBlend1 = [CCBlendMode blendModeWithOptions:@{
                                                                       CCBlendFuncSrcColor: @(GL_DST_COLOR),
                                                                       CCBlendFuncDstColor: @(GL_SRC_COLOR),
                                                                       }];
        CCBlendMode *lightBlend2 = [CCBlendMode blendModeWithOptions:@{
                                                                       CCBlendFuncSrcColor: @(GL_DST_COLOR),
                                                                       CCBlendFuncDstColor: @(GL_SRC_COLOR),
                                                                       }];
        CCBlendMode *lightBlend3 = [CCBlendMode blendModeWithOptions:@{
                                                                       CCBlendFuncSrcColor: @(GL_DST_COLOR),
                                                                       CCBlendFuncDstColor: @(GL_SRC_COLOR),
                                                                       }];

        _bgSpectrum.blendMode = lightBlend0;
        _bgNoise1.blendMode = lightBlend1;
        _bgNoise2.blendMode = lightBlend2;
        _bgNoise3.blendMode = lightBlend3;

        [_backgroundLayer addChild:_bgSpectrum];
        [_backgroundLayer addChild:_bgNoise1];
        [_backgroundLayer addChild:_bgNoise2];
        [_backgroundLayer addChild:_bgNoise3];

        _bgSpectrum.rotation = _bgSpectrum.currentAngle = arc4random_uniform(360);
        _bgNoise1.rotation = _bgNoise1.currentAngle = arc4random_uniform(360);
        _bgNoise2.rotation = _bgNoise2.currentAngle = arc4random_uniform(360);
        _bgNoise3.rotation = _bgNoise3.currentAngle = arc4random_uniform(360);

// End of nebula background setup
