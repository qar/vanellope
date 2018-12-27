/* eslint-disable */
import CodeMirror from 'codemirror';
window.CodeMirror = CodeMirror;
import * as _ from 'lodash';
import showdown from 'showdown';
import youtubeExt from '../../extensions/youtube-md';

showdown.extension('youtube', youtubeExt);
const converter = new showdown.Converter({
  // https://github.com/showdownjs/showdown/wiki/Showdown-options
  simplifiedAutoLink: true,
  strikethrough: true,
  tables: true,
  parseImgDimensions: true,
  tasklists: true,
  encodeEmails: true,
  extensions: ['youtube'],
});
import apis from '@/utils/api';
import $http from '@/utils/http';
import toMarkdown from 'to-markdown';

export default {
  name: 'MarkdownEditor',

  data() {
    return {
      // CodeMirror Options
      options: {
        // 编辑器模式: Github Flavor Markdown
        mode: 'gfm',

        // 是否自动折行
        lineWrapping: true,

        // 是否显示行号
        lineNumbers: false, // true or false

        // 滚动条样式
        scrollbarStyle: 'null', // native, null

        // 自动获取焦点
        autofocus: true,

        dragDrop: false,
      },

      modals: {
        categoryModal: false,
      },

      categories: [
        'default',
        'love',
      ],

      // 设置选项
      settings: {
        // 文章标题
        title: '',

        // 文章分类
        category: '',

        // 文章 id (可以用来判断是创建还是更新)
        uuid: '',

        select: '',
        radio: 'male',
        checkbox: [],
        switch: true,
        date: '',
        time: '',
        slider: [20, 50],
        textarea: ''
      },

      article: null,

      // in editing or in preview, or in settings
      section: 'edit',

      isPublishing: false,

      html: '',
    };
  },

  // boot-up
  mounted() {
    this.editor = new CodeMirror(this.$el, this.options);
    if (this.article) {
      if (this.article.ext === 'html') {
        this.editor.setValue(toMarkdown(this.article.content));
      } else {
        this.editor.setValue(this.article.source);
      }

      this.editor.refresh();
    }

    this.editor.on('paste', (cm, ev) => {
      if (!ev.clipboardData.files.length) return;
      const file = ev.clipboardData.files[0];
      if (file) {
        if (!file.type.startsWith('image/')) return;
        this.uploadFile(file);
        ev.preventDefault(); // so it won't paste file name
      }
    });
  },

  computed: {
    isInEditMode() {
      return this.section === 'edit' ? 'info' : 'ghost';
    },

    isInPreviewMode() {
      return this.section === 'preview' ? 'info' : 'ghost';
    },
  },

  created() {
    if (this.$route.params.articleId) {
      apis.getArticle(this.$route.params.articleId)
        .then(res => {
          this.article = res;
          this.settings.title = this.article.title;
          this.settings.uuid = this.article.uuid;

          if (this.editor) {
            if (this.article.ext === 'html') {
              this.editor.setValue(toMarkdown(this.article.content));
            } else { // Markdown
              this.editor.setValue(this.article.source);
            }

            this.editor.refresh();
          }
        });
    }
  },

  methods: {
    uploadFile(file) {
      const formData = new FormData();
      formData.append('image', file);
      $http.post('/api/v1/image', formData).then(res => {
        const doc = this.editor.getDoc();
        const cursor = doc.getCursor();
        var line = doc.getLine(cursor.line);
        var pos = { // create a new object to avoid mutation of the original selection
            line: cursor.line,
            ch: line.length  // set the character position to the end of the line
        };
        const mdImage = `![](${res.data.url})`;
        doc.replaceRange('\n' + mdImage + '\n', pos); // adds a new line
      });
    },

    preview() {
      // hide CodeMirror intance DOM
      const cmEle = this.editor.getWrapperElement();
      cmEle.classList.add('hide-cm-instance');

      // convert markdown to html and show on page
      const content = this.editor.getValue();
      this.html = converter.makeHtml(content);

      this.section = 'preview';
    },

    editing() {
      // show CodeMirror instance DOM
      const cmEle = this.editor.getWrapperElement();
      cmEle.classList.remove('hide-cm-instance');

      this.section = 'edit';
    },

    publish() {
      this.isPublishing = true;

      const source = this.editor.getValue();
      const content = converter.makeHtml(source);

      // use spliter or use first 300 characters as summary content
      let summary = '';
      const splitedSource = source.split(/<!--\s+more\s+-->/);
      const div = document.createElement('div');
      div.innerHTML = splitedSource.length > 1 ? converter.makeHtml(splitedSource[0]) : content;
      summary = (div.textContent || div.innerText || '').substring(0, 300);

      const params = {
        category: this.settings.category,
        content,
        summary,
        source,
        title: this.settings.title,
        state: 'published',
        ext: 'markdown'
      };

      if (this.settings.uuid) {
        apis.updateArticle(this.settings.uuid, params)
          .then(() => {
            this.updateSucceedNotify();
          })
          .finally(() => this.isPublishing = false);
      } else {
        apis.createArticle(params)
          .then(() => {
            this.publishSucceedNotify();
          })
          .finally(() => this.isPublishing = false);
      }
    },

    publishSucceedNotify() {
      this.$Notice.open({
        title: '新文章已创建',
        desc: '',
      });
    },

    updateSucceedNotify() {
      this.$Notice.open({
        title: '文章已更新',
        desc: '',
      });
    },
  },

  watch: {
    $route(newV, oldV) {
      if (newV.params.mode === 'new') {
        this.$Modal.confirm({
            title: '提醒',
            content: '当前文字正在编辑，是否保存？',
            loading: true,
            onOk: () => {
              localStorage.setItem('last-edit', JSON.stringify(this.article));
              localStorage.setItem('last-article-id', oldV.params.articleId);
              this.article = null;
              this.editor.setValue('');
              this.settings.title = '';
              this.$refs.title.focus();

              this.$Modal.remove();
              this.$Message.info('已保存');
            }
        });
      }
    },
  },
};
