'use client';

import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { Environment, Float, MeshTransmissionMaterial } from '@react-three/drei';
import { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';

// Mouse parallax camera rig
function CameraRig() {
    const { camera } = useThree();
    const mouse = useRef({ x: 0, y: 0 });

    useEffect(() => {
        const handleMouseMove = (event: MouseEvent) => {
            // Normalize mouse position to -1 to 1
            mouse.current.x = (event.clientX / window.innerWidth) * 2 - 1;
            mouse.current.y = -(event.clientY / window.innerHeight) * 2 + 1;
        };
        window.addEventListener('mousemove', handleMouseMove);
        return () => window.removeEventListener('mousemove', handleMouseMove);
    }, []);

    useFrame(() => {
        // Subtle parallax - camera follows mouse with easing
        camera.position.x = THREE.MathUtils.lerp(camera.position.x, mouse.current.x * 1.5, 0.02);
        camera.position.y = THREE.MathUtils.lerp(camera.position.y, mouse.current.y * 1, 0.02);
        camera.lookAt(0, 0, 0);
    });

    return null;
}

function Prisms() {
    const groupRef = useRef<THREE.Group>(null);

    // Slow continuous rotation for the entire group
    useFrame((state) => {
        if (groupRef.current) {
            groupRef.current.rotation.y = state.clock.elapsedTime * 0.02;
        }
    });

    return (
        <group ref={groupRef}>
            {/* Central Prism - The "Hero" Lens */}
            <Float speed={1.5} rotationIntensity={1.5} floatIntensity={1}>
                <mesh position={[0, 0, 0]} rotation={[0, 0, 0]} scale={2}>
                    <boxGeometry args={[1, 1, 1]} />
                    <MeshTransmissionMaterial
                        backside
                        samples={16}
                        thickness={200}
                        roughness={0.2}
                        chromaticAberration={1}
                        anisotropy={1}
                        distortion={0.5}
                        distortionScale={0.5}
                        temporalDistortion={0.2}
                        color="#050505"
                        background={new THREE.Color("#050505")}
                    />
                </mesh>
            </Float>

            {/* Floating Shards - More shards for richer atmosphere */}
            {[...Array(8)].map((_, i) => (
                <Float
                    key={i}
                    speed={0.8 + Math.random() * 0.5}
                    rotationIntensity={1.5}
                    floatIntensity={1.5}
                    position={[
                        (Math.random() - 0.5) * 14,
                        (Math.random() - 0.5) * 10,
                        (Math.random() - 0.5) * 8 - 2
                    ]}
                >
                    <mesh scale={0.3 + Math.random() * 0.5}>
                        <octahedronGeometry />
                        <MeshTransmissionMaterial
                            backside
                            samples={8}
                            thickness={40}
                            roughness={0.05}
                            chromaticAberration={0.8}
                            anisotropy={0.6}
                            color={i % 2 === 0 ? "#002FA7" : "#00D9FF"}
                            emissive={i % 2 === 0 ? "#002FA7" : "#00D9FF"}
                            emissiveIntensity={0.15}
                        />
                    </mesh>
                </Float>
            ))}

            {/* Volumetric light beams - Subtle spotlights */}
            <mesh position={[-5, 8, -5]} rotation={[0.5, 0, 0]}>
                <coneGeometry args={[3, 20, 32, 1, true]} />
                <meshBasicMaterial
                    color="#002FA7"
                    transparent
                    opacity={0.02}
                    side={THREE.DoubleSide}
                />
            </mesh>
            <mesh position={[6, -6, -8]} rotation={[-0.3, 0.2, 0]}>
                <coneGeometry args={[2.5, 18, 32, 1, true]} />
                <meshBasicMaterial
                    color="#00D9FF"
                    transparent
                    opacity={0.015}
                    side={THREE.DoubleSide}
                />
            </mesh>
        </group>
    );
}

export default function CinematicBackground() {
    return (
        <div className="fixed inset-0 z-0 pointer-events-none">
            <Canvas
                camera={{ position: [0, 0, 15], fov: 35 }}
                gl={{ antialias: true, alpha: true }}
                dpr={[1, 1.5]} // Performance optimization
            >
                <color attach="background" args={['#050505']} />

                {/* Mouse-driven parallax */}
                <CameraRig />

                {/* Lighting - Cinema-grade */}
                <ambientLight intensity={0.3} />
                <spotLight
                    position={[10, 10, 10]}
                    angle={0.15}
                    penumbra={1}
                    intensity={1.5}
                    color="#002FA7"
                    castShadow
                />
                <spotLight
                    position={[-8, -5, 8]}
                    angle={0.2}
                    penumbra={0.8}
                    intensity={0.8}
                    color="#00D9FF"
                />
                <pointLight position={[-10, -10, -10]} intensity={0.5} color="#00D9FF" />

                <Environment preset="city" />

                <Prisms />

                {/* Subtle Fog to blend edges */}
                <fog attach="fog" args={['#050505', 8, 28]} />
            </Canvas>
        </div>
    );
}
