import React from 'react';
import { Shield, Zap, Heart, Download, Smartphone, Globe } from 'lucide-react';

export const Features: React.FC = () => {
  const features = [
    {
      icon: Shield,
      title: 'Secure & Private',
      description: 'Your downloads are processed securely without storing any personal data',
      color: 'text-green-400'
    },
    {
      icon: Zap,
      title: 'Lightning Fast',
      description: 'High-speed downloads with optimized servers for maximum performance',
      color: 'text-yellow-400'
    },
    {
      icon: Heart,
      title: 'Always Free',
      description: 'No registration, no hidden fees, completely free to use forever',
      color: 'text-red-400'
    },
    {
      icon: Download,
      title: 'Multiple Formats',
      description: 'Support for MP4, MP3, WebM and various quality options',
      color: 'text-blue-400'
    },
    {
      icon: Smartphone,
      title: 'Mobile Friendly',
      description: 'Works perfectly on all devices - desktop, tablet, and mobile',
      color: 'text-purple-400'
    },
    {
      icon: Globe,
      title: 'No Limits',
      description: 'Download unlimited videos without any restrictions or quotas',
      color: 'text-pink-400'
    }
  ];

  return (
    <section className="py-16">
      <div className="text-center mb-12">
        <h3 className="text-3xl font-bold text-white mb-4">
          Why Choose Our Downloader?
        </h3>
        <p className="text-gray-300 text-lg max-w-2xl mx-auto">
          Experience the best YouTube downloading service with premium features and unmatched reliability
        </p>
      </div>
      
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
        {features.map((feature, index) => (
          <div
            key={index}
            className="glass-card rounded-2xl p-6 hover:scale-105 transition-all duration-300 group"
          >
            <div className="flex flex-col items-center text-center space-y-4">
              <div className={`p-4 rounded-2xl bg-white/10 group-hover:bg-white/20 transition-all duration-300`}>
                <feature.icon className={`w-8 h-8 ${feature.color}`} />
              </div>
              <h4 className="text-xl font-bold text-white">{feature.title}</h4>
              <p className="text-gray-300 leading-relaxed">{feature.description}</p>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};