import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Cabbage',
  tagline: 'A framework for audio software development',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://rorywalsh.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/cabbage3docs/',
  deploymentBranch: 'gh-pages',
  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'cabbageaudio', // Usually your GitHub org/user name.
  projectName: 'cabbage3', // Usually your repo name.
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },


  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/rorywalsh/cabbage3docs/tree/main/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/rorywalsh/cabbage3docs/tree/main/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      defaultMode: 'light', // Set the default mode (optional)
      disableSwitch: true,   // Disable the dark/light mode switch
    },
    navbar: {
      hideOnScroll: true, // Hide navbar on scroll
      items: [] // Empty array hides the navbar
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['csharp'],
    },
  } satisfies Preset.ThemeConfig,
  // Register the custom plugin
  plugins:
    [
      // Custom plugin to modify Webpack config
      function myCustomPlugin(context, options) {
        return {
          name: 'custom-webpack-plugin',
          configureWebpack(config, isServer, utils, content) {
            return {
              module: {
                rules: [
                  {
                    test: /\.csd$/,
                    type: 'asset/resource',
                  },
                ],
              },
            };
          },
        };
      },
    ],
};

export default config;
