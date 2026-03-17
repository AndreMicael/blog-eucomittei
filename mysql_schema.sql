-- ============================================================
-- Blog Dev Log - Schema MySQL (Hostgator)
-- Execute este arquivo pelo phpMyAdmin ou MySQL CLI
-- ============================================================

CREATE TABLE IF NOT EXISTS blog_posts (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    slug         VARCHAR(255) UNIQUE NOT NULL     COMMENT 'Identificador único do post (URL-friendly)',
    title        VARCHAR(500) NOT NULL             COMMENT 'Título gerado pela IA',
    content      LONGTEXT                          COMMENT 'Conteúdo Markdown completo',
    repo_name    VARCHAR(255)                      COMMENT 'Nome do repositório (ex: Sistema-Contratos-Frontend)',
    repo_url     VARCHAR(500)                      COMMENT 'URL do repositório no GitHub',
    categories   VARCHAR(500)                      COMMENT 'Categorias separadas por vírgula',
    tags         TEXT                              COMMENT 'Tags separadas por vírgula',
    commit_shas  TEXT                              COMMENT 'SHAs dos commits que geraram este post',
    post_date    DATE                              COMMENT 'Data do commit mais recente do grupo',
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Quando o post foi gerado',
    updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Índices úteis para consultas
CREATE INDEX IF NOT EXISTS idx_repo      ON blog_posts (repo_name);
CREATE INDEX IF NOT EXISTS idx_post_date ON blog_posts (post_date DESC);
